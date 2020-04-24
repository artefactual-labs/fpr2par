import os

from flask import flash

from fpr2par import app


def deletedbase():
    if os.path.isfile(app.db_name):
        os.remove("fpr2par.db")
        flash("database deleted")
    else:
        flash("database does not exist")
    return ()
