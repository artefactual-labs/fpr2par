from flask import Flask, render_template, flash, redirect, request
from fpr2par import app, db
import os
from .create_fpr_database import createdbase
from .add_fpr_data import adddata
from .delete_fpr_database import deletedbase
from datetime import datetime
from .models import (
    fpr_formats,
    fpr_format_groups,
    fpr_format_versions,
    fpr_id_tools,
    fpr_id_commands,
    fpr_id_rules,
    fpr_tools,
    fpr_commands,
    fpr_rules,
)


@app.route("/", methods=["GET"])
def home():
    if os.path.isfile("fpr2par.db"):
        formatGroups = fpr_format_groups.query.count()
        formats = fpr_formats.query.count()
        formatVersions = fpr_format_versions.query.count()
        idTools = fpr_id_tools.query.count()
        idCommands = fpr_id_commands.query.count()
        idRules = fpr_id_rules.query.count()
        tools = fpr_tools.query.count()
        commands = fpr_commands.query.count()
        rules = fpr_rules.query.count()
    else:
        formats = ""
        formatGroups = ""
        formatVersions = ""
        idTools = ""
        idCommands = ""
        idRules = ""
        tools = ""
        commands = ""
        rules = ""

    return render_template(
        "index.html",
        formatGroups=formatGroups,
        formats=formats,
        formatVersions=formatVersions,
        idTools=idTools,
        idCommands=idCommands,
        idRules=idRules,
        tools=tools,
        commands=commands,
        rules=rules,
    )


@app.route("/add_fpr_data", methods=["GET"])
def addFPRdata():
    duration = adddata()
    flash("FPR data loaded")
    flash("Import duration: " + duration)
    return redirect("/")


@app.route("/create_fpr_database", methods=["GET"])
def createFPRdbase():
    createdbase()
    return redirect("/")


@app.route("/delete_fpr_database", methods=["GET"])
def deleteFPRdata():
    deletedbase()
    return redirect("/")
