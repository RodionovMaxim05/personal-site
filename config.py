import os
import pathlib

SQLITE_DATABASE_NAME = "flask_auth.db"
SQLITE_DATABASE_BACKUP_NAME = "flask_auth.db.bak"

SECRET_KEY_FILE = os.path.join(pathlib.Path(__file__).parent, "flask_auth.conf")
SECRET_KEY = ""

if os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, "r") as file:
        SECRET_KEY = file.read().rstrip()
else:
    print("generate secret key")
    SECRET_KEY = os.urandom(16).hex()
