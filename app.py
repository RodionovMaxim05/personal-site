import os, requests
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from config import SQLITE_DATABASE_NAME, SECRET_KEY
from module import db, init_db, User, Counter
from flask_login import (
    login_user,
    LoginManager,
    current_user,
)


app = Flask(__name__, static_folder="static", template_folder="templates")

# SQLAlchimy config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + SQLITE_DATABASE_NAME
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SESSION_COOKIE_NAME"] = "se_session"

db.app = app
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login_page"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/send_respect", methods=["POST"])
def send_respect():
    if not current_user.is_authenticated:
        return jsonify({"message:": "Unauthorized"}), 401

    data = request.get_json()
    user_id = data.get("user_id")
    user = User.query.get(user_id)

    counter = Counter.query.first()

    if user and (not user.like):
        counter.increment()
        user.like = True
        db.session.commit()

    return jsonify({"message": "User like updated successfully"}), 200


@app.route("/get_count", methods=["GET"])
def get_count():
    counter = Counter.query.first()
    return jsonify({"count": counter.count}), 200


@app.route("/")
def index():
    user_id = session.get("user_id")
    user = User.query.get(user_id) if user_id else User(avatar_uri="static/img/cat.jpg")

    return render_template("index.html", user=user)


@app.route("/login")
def login_page():
    return render_template("login.html", ya_client_id=os.getenv("YANDEX_CLIENT_ID"))


def save_user(user):
    try:
        db.session.commit()
        session["user_id"] = user.id
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    login_user(user)


@app.route("/login/telegram")
def login_telegram():
    data = {
        "id": request.args.get("id", None),
        "first_name": request.args.get("first_name", None),
        "last_name": request.args.get("last_name", None),
        "username": request.args.get("username", None),
        "photo_url": request.args.get("photo_url", None),
        "auth_date": request.args.get("auth_date", None),
        "hash": request.args.get("hash", None),
    }

    user = User.query.filter_by(telegram_id=data["id"]).first()
    if user is None:
        user = User(
            telegram_id=data["id"],
            nick=data["first_name"],
            avatar_uri=data.get("photo_url"),
        )
        db.session.add(user)
    else:
        user.avatar_uri = data.get("photo_url", user.avatar_uri)

    save_user(user)
    return redirect(url_for("index"))


@app.route("/login/ya_auth")
def ya_auth():
    client_id = os.getenv("YANDEX_CLIENT_ID")
    client_secret = os.getenv("YANDEX_CLIENT_SECRET")
    oauth_url = (
        "https://oauth.yandex.ru/authorize?response_type=code&client_id=" + client_id
    )

    code = request.args.get("code")
    if code is None:
        return redirect(oauth_url)

    token_response = requests.post(
        "https://oauth.yandex.ru/token",
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        },
    )
    token_data = token_response.json()

    access_token = token_data["access_token"]
    user_info_response = requests.get(
        "https://login.yandex.ru/info?",
        headers={"Authorization": f"OAuth {access_token}"},
    )
    data = user_info_response.json()

    user = User.query.filter_by(yandex_id=data["id"]).first()
    if user is None:
        user = User(
            yandex_id=data["id"],
            nick=data["display_name"],
            avatar_uri=(
                f"https://avatars.yandex.net/get-yapic/{data['default_avatar_id']}/islands-200"
            ),
        )
        db.session.add(user)
    else:
        user.avatar_uri = f"https://avatars.yandex.net/get-yapic/{data['default_avatar_id']}/islands-200"

    save_user(user)
    return redirect(url_for("index"))


if __name__ == "__main__":
    db_file = Path("instance/" + SQLITE_DATABASE_NAME)

    if not os.path.exists(db_file):
        init_db(app)

    app.run(host="0.0.0.0", debug=True)
