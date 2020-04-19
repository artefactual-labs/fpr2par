import os
from flask import flash

def deletedbase():
    if os.path.isfile("fpr2par.db"):
        os.remove("fpr2par.db")
        flash("database deleted")
    else:
        flash("database does not exist")
    return ()
