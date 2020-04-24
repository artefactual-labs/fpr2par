from flask import Flask, render_template, flash, redirect, request, jsonify
from flask_basicauth import BasicAuth
from fpr2par import app, db
import os
from .create_fpr2par_database import createdbase
from .add_fpr2par_data import adddata
from .delete_fpr2par_database import deletedbase
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
    par_preservation_action_types,
)

from .helpers import _parse_offset_limit

basic_auth = BasicAuth(app)


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


@app.route("/admin", methods=["GET"])
@basic_auth.required
def admin():
    return render_template("admin.html")


@app.route("/create_fpr2par_database", methods=["GET"])
@basic_auth.required
def createfpr2pardbase():
    createdbase()
    return redirect("/admin")


@app.route("/add_fpr2par_data", methods=["GET"])
@basic_auth.required
def addFPRdata():
    duration = adddata()
    flash("FPR and PAR data loaded")
    flash("Import duration: " + duration)
    return redirect("/admin")


@app.route("/delete_fpr2par_database", methods=["GET"])
@basic_auth.required
def deletedfpr2pardbase():
    deletedbase()
    return redirect("/admin")


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


@app.route("/fpr_id_tools", methods=["GET"])
def fprIdTools():
    idTools = fpr_id_tools.query.all()
    count = fpr_id_tools.query.count()
    return render_template("fpr_id_tools.html", idTools=idTools, count=count)


@app.route("/fpr_id_command/<id>", methods=["GET"])
def fprIdCommand(id):
    idCommands = fpr_id_commands.query.filter_by(id_tool=id).all()
    count = fpr_id_commands.query.filter_by(id_tool=id).count()
    idTool = fpr_id_tools.query.get(id)
    return render_template(
        "fpr_id_command.html", idCommands=idCommands, idTool=idTool, count=count
    )


@app.route("/fpr_id_commands", methods=["GET"])
def fprIdCommands():
    idCommands = fpr_id_commands.query.all()
    count = fpr_id_commands.query.count()
    return render_template("fpr_id_commands.html", idCommands=idCommands, count=count)


@app.route("/fpr_id_rules", methods=["GET"])
def fprIdRules():
    idRules = fpr_id_rules.query.all()
    count = fpr_id_rules.query.count()
    return render_template("fpr_id_rules.html", idRules=idRules, count=count)


@app.route("/fpr_tools", methods=["GET"])
def fprTools():
    tools = fpr_tools.query.all()
    count = fpr_tools.query.count()
    return render_template("fpr_tools.html", tools=tools, count=count)


@app.route("/fpr_commands", methods=["GET"])
def fprCommands():
    commands = fpr_commands.query.all()
    count = fpr_commands.query.count()
    return render_template("fpr_commands.html", commands=commands, count=count)


@app.route("/fpr_command/<id>", methods=["GET"])
def fprCommand(id):
    commands = fpr_commands.query.filter_by(tool=id).all()
    count = fpr_commands.query.filter_by(tool=id).count()
    tool = fpr_tools.query.get(id)
    return render_template(
        "fpr_command.html", commands=commands, tool=tool, count=count
    )


@app.route("/fpr_rules", methods=["GET"])
def fprRules():
    rules = fpr_rules.query.all()
    count = fpr_rules.query.count()
    return render_template("fpr_rules.html", rules=rules, count=count)


@app.route("/fpr_rule/<id>", methods=["GET"])
def fprRule(id):
    rules = fpr_rules.query.filter_by(command=id).all()
    count = fpr_rules.query.filter_by(command=id).count()
    command = fpr_commands.query.get(id)
    return render_template("fpr_rule.html", rules=rules, command=command, count=count)


@app.route("/api/par/format-families/<guid>", methods=["GET"])
def formatFamily(guid):
    """
    Given a Format family's GUID, display information about it from the Format Policy Registry

    * <uri>/api/par/format-families/c94ce0e6-c275-4c09-b802-695a18b7bf2a

    """

    formatGroup = fpr_format_groups.query.get(guid)
    formats = fpr_formats.query.filter_by(group=formatGroup.uuid).all()
    newFormatVersions = []
    for format in formats:
        formatVersions = fpr_format_versions.query.filter_by(format=format.uuid).all()

        for formatVersion in formatVersions:
            if formatVersion.pronom_id != "":
                newFormatVersion = {
                    "guid": formatVersion.uuid,
                    "name": formatVersion.pronom_id,
                    "namespace": "http://www.nationalarchives.gov.uk",
                }
            else:
                newFormatVersion = {
                    "guid": formatVersion.uuid,
                    "name": formatVersion.description,
                    "namespace": "https://www.archivematica.org",
                }
            newFormatVersions.append(newFormatVersion)

        response = {
            "familyType": "Format Group",
            "id": {
                "guid": formatGroup.uuid,
                "name": formatGroup.description,
                "namespace": "https://archivematica.org",
            },
            "fileFormats": newFormatVersions,
        }

    return jsonify(response)


@app.route("/api/par/format-families", methods=["GET"])
def formatFamilies():
    """
    Display all Format families in the Format Policy Registry

    * <uri>/api/par/format-families/

    Alternatively, limit by count and offset:

    * <uri>/api/par/format-families?limit=1&offset=10
    """

    offset, limit = _parse_offset_limit(request)

    formatGroups = fpr_format_groups.query.all()[offset:limit]
    response = {}
    response["formatFamilies"] = []

    for formatGroup in formatGroups:
        formats = fpr_formats.query.filter_by(group=formatGroup.uuid).all()
        newFormatVersions = []
        for format in formats:
            formatVersions = fpr_format_versions.query.filter_by(
                format=format.uuid
            ).all()

            for formatVersion in formatVersions:
                if formatVersion.pronom_id != "":
                    newFormatVersion = {
                        "guid": formatVersion.uuid,
                        "name": formatVersion.pronom_id,
                        "namespace": "http://www.nationalarchives.gov.uk",
                    }
                else:
                    newFormatVersion = {
                        "guid": formatVersion.uuid,
                        "name": formatVersion.description,
                        "namespace": "https://www.archivematica.org",
                    }
                newFormatVersions.append(newFormatVersion)

        newGroup = {
            "familyType": "Format Group",
            "id": {
                "guid": formatGroup.uuid,
                "name": formatGroup.description,
                "namespace": "https://archivematica.org",
            },
            "fileFormats": newFormatVersions,
        }
        response["formatFamilies"].append(newGroup)

    return jsonify(response)


@app.route("/api/par/file-formats/<guid>", methods=["GET"])
def fileformat(guid):
    """
    Given a File format's GUID, display information about it from the Format Policy Registry

    * <uri>/api/par/file-formats/43d60a83-929a-45b4-9197-46177f85d095
    """

    version = fpr_format_versions.query.get(guid)
    format = fpr_formats.query.get(version.format)
    group = fpr_format_groups.query.get(format.group)

    if version.pronom_id != "":
        id = {
            "guid": version.uuid,
            "name": version.pronom_id,
            "namespace": "http://www.nationalarchives.gov.uk",
        }
        identifier = {
            "identifier": version.pronom_id,
            "identifierType": "PUID",
        }
    else:
        id = {
            "guid": version.uuid,
            "name": version.description,
            "namespace": "https://archivematica.org",
        }
        identifier = {
            "identifier": version.description,
            "identifierType": "Archivematica description",
        }
    if version.version == "":
        updatedVersion = None
    else:
        updatedVersion = version.version

    response = {
        "name": version.description,
        "localLastModifiedDate": str(version.last_modified),
        "version": updatedVersion,
        "id": id,
        "identifiers": [identifier],
        "types": [group.description],
    }

    return jsonify(response)


@app.route("/api/par/file-formats", methods=["GET"])
def fileformats():
    """
    Display all File formats in the Format Policy Registry

    * <uri>/api/par/file-formats/

    Alternatively, limit by count and offset:

    * <uri>/api/par/file-formats?limit=1&offset=10
    """

    offset, limit = _parse_offset_limit(request)

    versions = fpr_format_versions.query.all()[offset:limit]
    response = {}
    response["fileFormats"] = []

    for version in versions:
        format = fpr_formats.query.get(version.format)
        group = fpr_format_groups.query.get(format.group)
        if version.pronom_id != "":
            id = {
                "guid": version.uuid,
                "name": version.pronom_id,
                "namespace": "http://www.nationalarchives.gov.uk",
            }
            identifier = {
                "identifier": version.pronom_id,
                "identifierType": "PUID",
            }
        else:
            id = {
                "guid": version.uuid,
                "name": version.description,
                "namespace": "https://archivematica.org",
            }
            identifier = {
                "identifier": version.description,
                "identifierType": "Archivematica description",
            }
        if version.version == "":
            updatedVersion = None
        else:
            updatedVersion = version.version

        newFormat = {
            "name": version.description,
            "localLastModifiedDate": str(version.last_modified),
            "version": updatedVersion,
            "id": id,
            "identifiers": [identifier],
            "types": [group.description],
        }

        response["fileFormats"].append(newFormat)

    return jsonify(response)


@app.route("/api/par/preservation-action-types/<guid>", methods=["GET"])
def preservationActionType(guid):
    """
    Given a Preservation action type's GUID, display information about it from the fpr2par database

    * <uri>/api/par/preservation-action-types/d3c7ef45-5c58-4897-b145-d41afbf82c61
    """

    actionType = par_preservation_action_types.query.get(guid)
    response = {
        "id": {
            "guid": actionType.uuid,
            "name": actionType.name,
            "namespace": actionType.namespace,
        },
        "label": actionType.label,
        "localLastModifiedDate": str(actionType.last_modified),
    }

    return jsonify(response)


@app.route("/api/par/preservation-action-types", methods=["GET"])
def preservationActionTypes():
    """
    Display all Preservation action types in fpr2par

    * <uri>/api/par/preservation-action-types/

    Alternatively, limit by count and offset:

    * <uri>/api/par/preservation-action-types?limit=3&offset=0
    """

    offset, limit = _parse_offset_limit(request)

    response = {}
    response["preservationActionTypes"] = []
    actionTypes = par_preservation_action_types.query.all()[offset:limit]
    for actionType in actionTypes:
        newAction = {
            "id": {
                "guid": actionType.uuid,
                "name": actionType.name,
                "namespace": actionType.namespace,
            },
            "label": actionType.label,
            "localLastModifiedDate": str(actionType.last_modified),
        }
        response["preservationActionTypes"].append(newAction)
    return jsonify(response)


@app.route("/api/par/preservation-actions/<guid>", methods=["GET"])
def preservationAction(guid):
    return jsonify({"response": "Not implemented"})


@app.route("/api/par/preservation-actions", methods=["GET"])
def preservationActions():
    return jsonify({"response": "Not implemented"})


@app.route("/api/par/tools/<guid>", methods=["GET"])
def tool(guid):
    """
    Given a Tool's GUID, display information about it from the Format Policy Registry

    * <uri>/api/par/tools/246ad3d4-6a5d-466b-a35c-26c1323d198e
    """

    response = {}
    tool = fpr_tools.query.get(guid)
    if tool is not None:
        response = {
            "id": {
                "guid": tool.uuid,
                "name": tool.slug,
                "namespace": "https://archivematica.org",
            },
            "toolName": tool.description,
            "toolVersion": tool.version,
        }
    else:
        # check whether the GUID matches an Identification tool
        tool = fpr_id_tools.query.get(guid)
        if tool is not None:
            response = {
                "id": {
                    "guid": tool.uuid,
                    "name": tool.slug,
                    "namespace": "https://archivematica.org",
                },
                "toolName": tool.description,
                "toolVersion": tool.version,
            }

    return jsonify(response)


@app.route("/api/par/tools", methods=["GET"])
def tools():
    """
    Display all Tools in the Format Policy Registry

    * <uri>/api/par/tools/
    """

    response = {}
    response["tools"] = []
    # only include enabled tools
    tools = fpr_tools.query.filter_by(enabled=True).all()

    for tool in tools:
        newTool = {
            "id": {
                "guid": tool.uuid,
                "name": tool.slug,
                "namespace": "https://archivematica.org",
            },
            "toolName": tool.description,
            "toolVersion": tool.version,
        }
        response["tools"].append(newTool)

    # include Identification tools
    # only include enabled tools
    tools = fpr_id_tools.query.filter_by(enabled=True).all()
    for tool in tools:
        newTool = {
            "id": {
                "guid": tool.uuid,
                "name": tool.slug,
                "namespace": "https://archivematica.org",
            },
            "toolName": tool.description,
            "toolVersion": tool.version,
        }
        response["tools"].append(newTool)

    return jsonify(response)


@app.route("/api/par/business-rules/<guid>", methods=["GET"])
def businessRule(guid):
    return jsonify({"response": "Not implemented"})
