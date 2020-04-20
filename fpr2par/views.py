from flask import Flask, render_template, flash, redirect, request, jsonify
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

    apiUrl = request.base_url + "api/par"

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
        apiUrl=apiUrl,
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


@app.route("/fpr_format_groups", methods=["GET"])
def fprFormatGroups():
    formatGroups = fpr_format_groups.query.all()
    count = fpr_format_groups.query.count()
    return render_template(
        "fpr_format_groups.html", formatGroups=formatGroups, count=count
    )


@app.route("/fpr_format_group/<id>", methods=["GET"])
def fprFormatGroup(id):
    formats = fpr_formats.query.filter_by(group=id).all()
    formatGroup = fpr_format_groups.query.get(id)
    return render_template(
        "fpr_format_group.html", formats=formats, formatGroup=formatGroup
    )


@app.route("/fpr_formats", methods=["GET"])
def fprFormats():
    formats = fpr_formats.query.all()
    count = fpr_formats.query.count()
    return render_template("fpr_formats.html", formats=formats, count=count)


@app.route("/fpr_format_version/<id>", methods=["GET"])
def fprFormatVersion(id):
    versions = fpr_format_versions.query.filter_by(format=id).all()
    format = fpr_formats.query.get(id)
    return render_template("fpr_format_version.html", format=format, versions=versions)


@app.route("/fpr_format_versions", methods=["GET"])
def fprFormatVersions():
    versions = fpr_format_versions.query.all()
    count = fpr_format_versions.query.count()
    return render_template("fpr_format_versions.html", versions=versions, count=count)


@app.route("/api/par/file-formats/<id>", methods=["GET"])
def fileformat(id):
    version = fpr_format_versions.query.get(id)
    format = fpr_formats.query.get(version.format)
    group = fpr_format_groups.query.get(format.group)
    response = {
        "name": version.description,
        "localLastModifiedDate": str(version.last_modified),
        "version": version.version,
        "id": {"guid": version.uuid, "namespace": "https://archivematica.org"},
        "identifiers": {"identifier": version.pronom_id, "identifierType": "PUID"},
        "type": group.description,
    }
    return jsonify(response)
