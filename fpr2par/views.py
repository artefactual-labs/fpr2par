from flask import Flask, render_template, flash, redirect, request, jsonify
from flask_basicauth import BasicAuth
from slugify import slugify
import os
from fpr2par import app, db
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

from .helpers import (
    # Parse functions associated with various API filter options.
    _parse_filter_dates,
    _parse_filter_headers,
    _parse_offset_limit,
    # Filter values associated with various API filter options.
    GUID_HEADER,
    FILE_FORMAT_HEADER,
    PRESERVATION_ACT_HEADER,
    TOOL_HEADER,
)

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

            if formatVersion.pronom_id:
                formatName = formatVersion.pronom_id
                if formatVersion.pronom_id[:3] == "arc":
                    formatNamespace = "https://archivematica.org"
                else:
                    formatNamespace = "http://www.nationalarchives.uk.gov"
            else:
                formatName = slugify(formatVersion.description)
                formatNamespace = "https://archivematica.org"

            newFormatVersion = {
                "guid": formatVersion.uuid,
                "name": formatName,
                "namespace": formatNamespace,
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
                if formatVersion.pronom_id:
                    formatName = formatVersion.pronom_id
                    if formatVersion.pronom_id[:3] == "arc":
                        formatNamespace = "https://archivematica.org"
                    else:
                        formatNamespace = "http://www.nationalarchives.uk.gov"
                else:
                    formatName = slugify(formatVersion.description)
                    formatNamespace = "https://archivematica.org"

                newFormatVersion = {
                    "guid": formatVersion.uuid,
                    "name": formatName,
                    "namespace": formatNamespace,
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

    if version.pronom_id:
        if version.pronom_id[:3] == "arc":
            namespace = "https://archivematica.org"
        else:
            namespace = "http://www.nationalarchives.uk.gov"
        id = {
            "guid": version.uuid,
            "name": version.pronom_id,
            "namespace": namespace,
        }
        identifier = {
            "identifier": version.pronom_id,
            "identifierType": "PUID",
        }
    else:
        id = {
            "guid": version.uuid,
            "name": slugify(version.description),
            "namespace": "https://archivematica.org",
        }
        identifier = {
            "identifier": slugify(version.description),
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

    As well as limit by modified before and after dates (both optional)

    * <uri>/api/par/file-formats?modified-before=2020-01-01&modified-after=1970-01-01

    """

    offset, limit = _parse_offset_limit(request)
    before_date, after_date = _parse_filter_dates(request)

    # Filter parsing using request headers.
    headers = _parse_filter_headers(request)
    format_filter = headers.get(FILE_FORMAT_HEADER, None)

    versions = fpr_format_versions.query.filter(
        fpr_format_versions.last_modified.between(after_date, before_date)
    ).all()[offset:limit]

    response = {}
    response["fileFormats"] = []

    for version in versions:

        if format_filter != [] and version.pronom_id not in format_filter:
            continue

        file_format = fpr_formats.query.get(version.format)
        group = fpr_format_groups.query.get(file_format.group)
        if version.pronom_id:
            if version.pronom_id[:3] == "arc":
                namespace = "https://archivematica.org"
            else:
                namespace = "http://www.nationalarchives.uk.gov"
            id = {
                "guid": version.uuid,
                "name": version.pronom_id,
                "namespace": namespace,
            }
            identifier = {
                "identifier": version.pronom_id,
                "identifierType": "PUID",
            }
        else:
            id = {
                "guid": version.uuid,
                "name": slugify(version.description),
                "namespace": "https://archivematica.org",
            }
        identifier = {
            "identifier": slugify(version.description),
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

    As well as limit by modified before and after dates (both optional)

    * <uri>/api/par/preservation-action-types?modified-before=2020-01-01&modified-after=1970-01-01

    """

    offset, limit = _parse_offset_limit(request)
    before_date, after_date = _parse_filter_dates(request)

    response = {}
    response["preservationActionTypes"] = []

    actionTypes = par_preservation_action_types.query.filter(
        par_preservation_action_types.last_modified.between(after_date, before_date)
    ).all()[offset:limit]

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
    """
    Given a Preservation action's GUID, display information about it from the fpr2par database

    * <uri>/api/par/preservation-actions/1628571b-c2cd-4822-afdb-53561400c7c4
    """
    action = fpr_commands.query.get(guid)
    if action:
        action_type = par_preservation_action_types.query.filter_by(
            label=action.command_usage.lower()
        ).first()
        tool = fpr_tools.query.get(action.tool)
        action_label = action.command_usage.lower()
        action_command = action.command

        constraints = []
        rules = fpr_rules.query.filter_by(command=action.uuid, enabled=True).all()

        if not rules:
            # check to see if we're dealing with an event_detail command
            commands = fpr_commands.query.filter_by(
                event_detail_command=action.uuid, enabled=True
            ).all()
            if commands:
                for command in commands:
                    rules = (
                        rules
                        + fpr_rules.query.filter_by(
                            command=command.uuid, enabled=True
                        ).all()
                    )
        if not rules:
            # check to see if we're dealing with a verification command
            commands = fpr_commands.query.filter_by(
                verification_command=action.uuid, enabled=True
            )
            if commands:
                for command in commands:
                    rules = (
                        rules
                        + fpr_rules.query.filter_by(
                            command=command.uuid, enabled=True
                        ).all()
                    )
        if rules:
            for rule in rules:
                version = fpr_format_versions.query.filter_by(uuid=rule.format).first()
                if version.pronom_id:
                    if version.pronom_id[:3] == "arc":
                        namespace = "https://archivematica.org"
                    else:
                        namespace = "http://www.nationalarchives.uk.gov"
                    id = {
                        "guid": version.uuid,
                        "name": version.pronom_id,
                        "namespace": namespace,
                    }
                else:
                    id = {
                        "guid": version.uuid,
                        "name": slugify(version.description),
                        "namespace": "https://archivematica.org",
                    }
                constraints.append(
                    {"id": id, "localLastModifiedDate": str(version.last_modified),}
                )

        # a rough heuristic for determining inpuFiles names (since FPR does not
        # record this information separately)
        if "%inputFile%" in action.command:
            inputFile = "%inputFile"
        elif "%fileFullName" in action.command:
            inputFile = "%fileFullName%"
        elif "%relativeLocation%" in action.command:
            inputFile = "%relativeLocation"
        elif "$ocrfiles" in action.command:
            inputFile = "$ocrfiles"
        else:
            inputFile = "%inputFile%"
        inputFiles = {
            "description": "The file that will be acted upon",
            "name": inputFile,
        }

        # a rough heuristic for determining ouptFiles name (since FPR does not
        # record this information separately)
        if (action_type.name == "tra") or (action_type.name == "nor"):
            outputFiles = {
                "description": "The file that will be created",
                "name": action.output_location,
            }
        elif action_type.name == "cha":
            if action.description == "FITS":
                outputFiles = {
                    "description": "The file that will be created",
                    "name": "fits.xml",
                }
            else:
                outputFiles = {
                    "description": "The file that will be created",
                    "name": "%fileFullName%.xml",
                }
        elif action_type.name in ("eve", "val", "ide"):
            outputFiles = {
                "description": "The file where output is recorded",
                "name": "METS.[AIP UUUD].xml",
            }
        elif action_type.name == "ext":
            outputFiles = {
                "description": "The file that will be extracted",
                "name": "%outputDirector%/%fileFullName%",
            }
        else:
            outputFiles = None

        response = {
            "constraints": {
                "items": {"properties": {"allowedFormats": {"items": constraints,},},},
            },
            "description": action.description,
            "example": action_command,
            "localLastModifiedDate": str(action.last_modified),
            "id": {
                "guid": action.uuid,
                "name": action.description,
                "namespace": "https://archivematica.org",
            },
            "tool": {
                "id": {
                    "guid": tool.uuid,
                    "name": tool.slug,
                    "namespace": "https://archivematica.org",
                },
                "toolName": tool.description,
                "toolVersion": tool.version,
            },
            "type": {
                "id": {
                    "guid": action_type.uuid,
                    "name": action_type.name,
                    "namespace": "https://archivematica.org",
                },
                "label": action_label,
            },
            "inputFiles": [inputFiles],
            "outputFiles": [outputFiles],
        }

    action = fpr_id_commands.query.get(guid)
    if action:
        type = par_preservation_action_types.query.get(
            "d3c7ef45-5c58-4897-b145-d41afbf82c61"
        )
        tool = fpr_id_tools.query.get(action.id_tool)

        constraints = "all"
        # get constraints if tool is ID by File Extension
        if action.uuid == "41efbe1b-3fc7-4b24-9290-d0fb5d0ea9e9":
            formats = fpr_id_rules.query.filter_by(
                command="41efbe1b-3fc7-4b24-9290-d0fb5d0ea9e9"
            )
            for version in formats:
                if version.pronom_id:
                    if version.pronom_id[:3] == "arc":
                        namespace = "https://archivematica.org"
                    else:
                        namespace = "http://www.nationalarchives.uk.gov"
                        id = {
                            "guid": version.uuid,
                            "name": version.pronom_id,
                            "namespace": namespace,
                        }
                else:
                    id = {
                        "guid": version.uuid,
                        "name": slugify(version.description),
                        "namespace": "https://archivematica.org",
                    }
                constraints.append(
                    {"id": id, "localLastModifiedDate": str(version.last_modified),}
                )

        response = {
            "constraints": {
                "items": {"properties": {"allowedFormats": {"items": constraints,},},},
            },
            "description": action.description,
            "example": action.script,
            "localLastModifiedDate": str(action.last_modified),
            "id": {
                "guid": action.uuid,
                "name": action.description,
                "namespace": "https://archivematica.org",
            },
            "tool": {
                "id": {
                    "guid": tool.uuid,
                    "name": tool.slug,
                    "namespace": "https://archivematica.org",
                },
                "toolName": tool.description,
                "toolVersion": tool.version,
            },
            "type": {
                "id": {
                    "guid": type.uuid,
                    "name": type.name,
                    "namespace": "https://archivematica.org",
                },
                "label": type.label,
            },
            "inputFiles": [
                {
                    "description": "The file that will be acted upon",
                    "name": "%inputFile%",
                }
            ],
            "outputFiles": [
                {
                    "description": "file where output is recorded",
                    "name": "METS.[AIP UUUD].xml",
                }
            ],
        }

    return jsonify(response)


@app.route("/api/par/preservation-actions", methods=["GET"])
def preservationActions():
    """
    Display all Preservation actions in fpr2par

    * <uri>/api/par/preservation-actions/

    Alternatively, limit by count and offset:

    * <uri>/api/par/preservation-actions?limit=3&offset=0

    As well as limit by modified before and after dates (both optional)

    * <uri>/api/par/preservation-actions?modified-before=2020-01-01&modified-after=1970-01-01

    """
    response = {}
    response["preservationActions"] = []

    offset, limit = _parse_offset_limit(request)
    before_date, after_date = _parse_filter_dates(request)

    # Filter parsing using request headers.
    headers = _parse_filter_headers(request)
    pres_act_filter = headers.get(PRESERVATION_ACT_HEADER, None)
    tool_filter = headers.get(TOOL_HEADER, None)
    guid_filter = headers.get(GUID_HEADER, None)

    dpActions = (
        fpr_commands.query.filter_by(enabled=True)
        .filter(fpr_commands.last_modified.between(after_date, before_date))
        .all()
    )

    dpIDActions = (
        fpr_id_commands.query.filter_by(enabled=True)
        .filter(fpr_id_commands.last_modified.between(after_date, before_date))
        .all()
    )

    all_actions = (dpActions + dpIDActions)[offset:limit]

    for action in all_actions:

        # While both sets of tools ("actions") sit independently of each other
        # we can use that to our advantage to determine which is which where
        # the models differ.
        try:
            # This is an ID tool so set ID action_type
            _ = action.id_tool
            action_type = par_preservation_action_types.query.get(
                "d3c7ef45-5c58-4897-b145-d41afbf82c61"
            )
            tool = fpr_id_tools.query.get(action.id_tool)
            action_label = action_type.label
            action_command = action.script
            inputFiles = {
                "description": "The file that will be acted upon",
                "name": "%inputFile%",
            }
            constraints = "all"
        except AttributeError:
            # We don't have an ID tool so set action type differently.
            action_type = par_preservation_action_types.query.filter_by(
                label=action.command_usage.lower()
            ).first()
            tool = fpr_tools.query.get(action.tool)
            action_label = action.command_usage.lower()
            action_command = action.command
            constraints = []

        # Apply header-based filtering.
        if guid_filter != [] and action.uuid not in guid_filter:
            continue
        if tool_filter != [] and tool.uuid not in tool_filter:
            continue
        if pres_act_filter != [] and action_type.uuid not in pres_act_filter:
            continue

        rules = fpr_rules.query.filter_by(command=action.uuid, enabled=True).all()

        if not rules:
            # check to see if we're dealing with an event_detail command
            commands = fpr_commands.query.filter_by(
                event_detail_command=action.uuid, enabled=True
            ).all()
            if commands:
                for command in commands:
                    rules = (
                        rules
                        + fpr_rules.query.filter_by(
                            command=command.uuid, enabled=True
                        ).all()
                    )
        if not rules:
            # check to see if we're dealing with a verification command
            commands = fpr_commands.query.filter_by(
                verification_command=action.uuid, enabled=True
            )
            if commands:
                for command in commands:
                    rules = (
                        rules
                        + fpr_rules.query.filter_by(
                            command=command.uuid, enabled=True
                        ).all()
                    )
        if rules:
            for rule in rules:
                version = fpr_format_versions.query.filter_by(uuid=rule.format).first()
                if version.pronom_id:
                    if version.pronom_id[:3] == "arc":
                        namespace = "https://archivematica.org"
                    else:
                        namespace = "http://www.nationalarchives.uk.gov"
                    id = {
                        "guid": version.uuid,
                        "name": version.pronom_id,
                        "namespace": namespace,
                    }
                else:
                    id = {
                        "guid": version.uuid,
                        "name": slugify(version.description),
                        "namespace": "https://archivematica.org",
                    }
                constraints.append(
                    {"id": id, "localLastModifiedDate": str(version.last_modified),}
                )

            # a rough heuristic for determining inpuFiles names (since FPR does not
            # record this information separately)
            if "%inputFile%" in action.command:
                inputFile = "%inputFile"
            elif "%fileFullName" in action.command:
                inputFile = "%fileFullName%"
            elif "%relativeLocation%" in action.command:
                inputFile = "%relativeLocation"
            elif "$ocrfiles" in action.command:
                inputFile = "$ocrfiles"
            else:
                inputFile = "%inputFile%"
            inputFiles = {
                "description": "The file that will be acted upon",
                "name": inputFile,
            }

        # a rough heuristic for determining ouptFiles name (since FPR does not
        # record this information separately)
        if (action_type.name == "tra") or (action_type.name == "nor"):
            outputFiles = {
                "description": "The file that will be created",
                "name": action.output_location,
            }
        elif action_type.name == "cha":
            if action.description == "FITS":
                outputFiles = {
                    "description": "The file that will be created",
                    "name": "fits.xml",
                }
            else:
                outputFiles = {
                    "description": "The file that will be created",
                    "name": "%fileFullName%.xml",
                }
        elif action_type.name in ("eve", "val", "ide"):
            outputFiles = {
                "description": "The file where output is recorded",
                "name": "METS.[AIP UUUD].xml",
            }
        elif action_type.name == "ext":
            outputFiles = {
                "description": "The file that will be extracted",
                "name": "%outputDirector%/%fileFullName%",
            }
        else:
            outputFiles = None

        newAction = {
            "constraints": {
                "items": {"properties": {"allowedFormats": {"items": constraints,},},},
            },
            "description": action.description,
            "example": action_command,
            "localLastModifiedDate": str(action.last_modified),
            "id": {
                "guid": action.uuid,
                "name": action.description,
                "namespace": "https://archivematica.org",
            },
            "tool": {
                "id": {
                    "guid": tool.uuid,
                    "name": tool.slug,
                    "namespace": "https://archivematica.org",
                },
                "toolName": tool.description,
                "toolVersion": tool.version,
            },
            "type": {
                "id": {
                    "guid": action_type.uuid,
                    "name": action_type.name,
                    "namespace": "https://archivematica.org",
                },
                "label": action_label,
            },
            "inputFiles": [inputFiles],
            "outputFiles": [outputFiles],
        }
        response["preservationActions"].append(newAction)

    return jsonify(response)


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

    Alternatively, limit by count and offset:

    * <uri>/api/par/tools?limit=3&offset=0

    """

    response = {}
    response["tools"] = []

    offset, limit = _parse_offset_limit(request)

    # Filter parsing using request headers.
    headers = _parse_filter_headers(request)
    tools_filter = headers.get(GUID_HEADER, None)

    # Only include enabled tools.
    tools = fpr_tools.query.filter_by(enabled=True)
    id_tools = fpr_id_tools.query.filter_by(enabled=True)

    # If we have a filter, only include tools that we've requested.
    if tools_filter != []:
        tools = tools.filter(fpr_tools.uuid.in_(tools_filter)).all()
        id_tools = id_tools.filter(fpr_id_tools.uuid.in_(tools_filter)).all()
    else:
        tools = tools.all()
        id_tools = id_tools.all()

    # concatenate our two lists.
    new_tools = (tools + id_tools)[offset:limit]

    for tool in new_tools:
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
    """
    Given a business rule's GUID, display information about it generated by add_fpr2par_data

    * <uri>/api/par/business-rules/<guid>
    """

    response = {}
    rule = fpr_rules.query.get(guid)
    command = fpr_commands.query.get(rule.command)
    format = fpr_format_versions.query.get(rule.format)
    if format.pronom_id:
        formatName = format.pronom_id
        if format.pronom_id[:3] == "arc":
            formatNamespace = "https://archivematica.org"
        else:
            formatNamespace = "http://www.nationalarchives.uk.gov"
    else:
        formatName = slugify(format.description)
        formatNamespace = "https://archivematica.org"
    name = (
        str(command.fprTool)
        + "-"
        + rule.purpose
        + "-"
        + format.description
        + "("
        + format.pronom_id
        + ")"
    )
    description = (
        "For "
        + rule.purpose
        + " of "
        + format.description
        + "("
        + format.pronom_id
        + "), use "
        + str(command.fprTool)
    )

    priority = 1
    preservationActions = []
    preservationActions.append(
        {
            "preservationAction": {
                "guid": command.uuid,
                "name": command.description,
                "namespace": "https://archivematica.org",
            },
            "priority": priority,
        }
    )
    if command.verification_command:
        priority += 1
        verificationCommand = fpr_commands.query.get(command.verification_command)
        preservationActions.append(
            {
                "preservationAction": {
                    "guid": verificationCommand.uuid,
                    "name": verificationCommand.description,
                    "namespace": "https://archivematica.org",
                },
                "priority": priority,
            }
        )
    if command.event_detail_command:
        priority += 1
        eventDetailCommand = fpr_commands.query.get(command.event_detail_command)
        preservationActions.append(
            {
                "preservationAction": {
                    "guid": eventDetailCommand.uuid,
                    "name": eventDetailCommand.description,
                    "namespace": "https://archivematica.org",
                },
                "priority": priority,
            }
        )

    actionType = par_preservation_action_types.query.filter_by(
        label=command.command_usage.lower()
    ).first()

    response = {
        "id": {
            "guid": rule.uuid,
            "name": name,
            "namespace": "https://archivematica.org",
        },
        "formats": [
            {"guid": format.uuid, "name": formatName, "namespace": formatNamespace}
        ],
        "preservationActions": preservationActions,
        "preservationActionTypes": [
            {
                "id": {
                    "guid": actionType.uuid,
                    "name": actionType.name,
                    "namespace": "https://archivematica.org",
                },
                "label": actionType.label,
            },
        ],
        "localLastModifiedDate": str(rule.last_modified),
        "description": description,
        "notes": "This rule has been automatically generated from Archivematica FPR values.",
    }

    return jsonify(response)


@app.route("/api/par/business-rules", methods=["GET"])
def businessRules():
    """
    Display all Business Rules generated by fpr2par

    * <uri>/api/par/business-rules/

    Alternatively, limit by count and offset:

    * <uri>/api/par/business-rules?limit=1&offset=10

    As well as limit by modified before and after dates (both optional)

    * <uri>/api/par/business-rules?modified-before=2020-01-01&modified-after=1970-01-01

    """

    offset, limit = _parse_offset_limit(request)
    before_date, after_date = _parse_filter_dates(request)

    # Filter parsing using request headers.
    headers = _parse_filter_headers(request)
    guid_filter = headers.get(GUID_HEADER, None)
    format_filter = headers.get(FILE_FORMAT_HEADER, None)
    pres_act_filter = headers.get(PRESERVATION_ACT_HEADER, None)

    rules = (
        fpr_rules.query.filter_by(enabled=True)
        .filter(fpr_rules.last_modified.between(after_date, before_date))
        .all()[offset:limit]
    )

    response = {}
    response["businessRules"] = []
    for rule in rules:
        command = fpr_commands.query.get(rule.command)
        file_format = fpr_format_versions.query.get(rule.format)
        if format_filter != [] and file_format.pronom_id not in format_filter:
            continue
        if guid_filter != [] and rule.uuid not in guid_filter:
            continue
        if file_format.pronom_id:
            formatName = file_format.pronom_id
            if file_format.pronom_id[:3] == "arc":
                formatNamespace = "https://archivematica.org"
            else:
                formatNamespace = "http://www.nationalarchives.uk.gov"
        else:
            formatName = slugify(file_format.description)
            formatNamespace = "https://archivematica.org"
        name = "{}-{}-{}({})".format(
            command.fprTool,
            rule.purpose,
            file_format.description.strip(),
            file_format.pronom_id,
        )
        description = "For {} of {} ({}), use {}".format(
            rule.purpose,
            file_format.description.strip(),
            file_format.pronom_id,
            command.fprTool,
        )
        priority = 1
        preservationActions = []
        preservationActions.append(
            {
                "preservationAction": {
                    "guid": command.uuid,
                    "name": command.description,
                    "namespace": "https://archivematica.org",
                },
                "priority": priority,
            }
        )
        if command.verification_command:
            priority += 1
            verificationCommand = fpr_commands.query.get(command.verification_command)
            preservationActions.append(
                {
                    "preservationAction": {
                        "guid": verificationCommand.uuid,
                        "name": verificationCommand.description,
                        "namespace": "https://archivematica.org",
                    },
                    "priority": priority,
                }
            )
        if command.event_detail_command:
            priority += 1
            eventDetailCommand = fpr_commands.query.get(command.event_detail_command)
            preservationActions.append(
                {
                    "preservationAction": {
                        "guid": eventDetailCommand.uuid,
                        "name": eventDetailCommand.description,
                        "namespace": "https://archivematica.org",
                    },
                    "priority": priority,
                }
            )

        actionType = par_preservation_action_types.query.filter_by(
            label=command.command_usage.lower()
        ).first()

        if pres_act_filter != [] and actionType.uuid not in pres_act_filter:
            continue

        newRule = {
            "id": {
                "guid": rule.uuid,
                "name": name,
                "namespace": "https://archivematica.org",
            },
            "formats": [
                {
                    "guid": file_format.uuid,
                    "name": formatName,
                    "namespace": formatNamespace,
                }
            ],
            "preservationActions": preservationActions,
            "preservationActionTypes": [
                {
                    "id": {
                        "guid": actionType.uuid,
                        "name": actionType.name,
                        "namespace": "https://archivematica.org",
                    },
                    "label": actionType.label,
                },
            ],
            "localLastModifiedDate": str(rule.last_modified),
            "description": description,
            "notes": "This rule has been automatically generated from Archivematica FPR values.",
        }
        response["businessRules"].append(newRule)

    return jsonify(response)
