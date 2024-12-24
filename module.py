from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from pathlib import Path
import shutil

from config import SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    nick = db.Column(db.String(255), nullable=True)
    avatar_uri = db.Column(db.String(255), default="static/img/cat.jpg", nullable=False)

    yandex_id = db.Column(db.String(255), nullable=True)
    telegram_id = db.Column(db.String(255), nullable=True)

    like = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self) -> str:
        return f"Id={self.id} - Nick={self.nick}"

    def __str__(self) -> str:
        return f"Id={self.id} - Nick={self.nick}"


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

    def increment(self):
        self.count += 1


def init_db(app):
    db_file = Path("instance/" + SQLITE_DATABASE_NAME)
    if db_file.is_file():
        shutil.copyfile("instance/" + SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME)

    with app.app_context():
        print("Create DB: " + app.config["SQLALCHEMY_DATABASE_URI"])
        db.session.commit()  # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
        db.drop_all()
        db.create_all()

        counter = Counter()
        db.session.add(counter)
        db.session.commit()
