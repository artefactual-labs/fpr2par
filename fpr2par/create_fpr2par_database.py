import os
from fpr2par import db
from flask import flash


def createdbase():
    if os.path.isfile("fpr2par.db"):
        flash("database already exists")
    else:
        db.create_all()
        flash("database created")
    return ()
