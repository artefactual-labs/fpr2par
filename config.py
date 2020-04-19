import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "fpr2par.db")
SQLALCHEMY_ECHO = False

SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
