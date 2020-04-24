import os
from fpr2par import app, db
from flask import flash


def createdbase():
    print(app.db_name)
    if os.path.isfile(app.db_name):
        flash("database already exists")
    else:
        db.create_all()
        flash("database created")
    return ()
