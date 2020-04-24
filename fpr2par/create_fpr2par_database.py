import os

from flask import flash

from fpr2par import app, db


def createdbase():
    if os.path.isfile(app.db_name):
        flash("database already exists")
    else:
        db.create_all()
        flash("database created")
    return ()
