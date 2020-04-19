from fpr2par import db
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
import json
from datetime import datetime
import os


def adddata():

    # track total FPR data load time
    start = datetime.now()

    # make sure files are sorted by name so data is entered in correct order
    for file in sorted(os.listdir("sourceJSON")):

        if file[-5:] == ".json":
            print("processing file: " + file)

            with open("sourceJSON/" + file, "r") as jsonFile:
                data = jsonFile.read()

            jsonObjects = json.loads(data)

            for object in jsonObjects:

                if object["model"] == "fpr.formatgroup":
                    output = object["model"] + " " + object["fields"]["description"]

                    formatGroup = fpr_format_groups(
                        uuid=object["fields"]["uuid"],
                        slug=object["fields"]["slug"],
                        description=object["fields"]["description"],
                    )

                    if (
                        fpr_format_groups.query.get(object["fields"]["uuid"])
                        is not None
                    ):
                        fpr_format_groups.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "slug": object["fields"]["slug"],
                                "description": object["fields"]["description"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(formatGroup)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.format":
                    output = object["model"] + " " + object["fields"]["description"]

                    format = fpr_formats(
                        uuid=object["fields"]["uuid"],
                        group=object["fields"]["group"],
                        slug=object["fields"]["slug"],
                        description=object["fields"]["description"],
                    )

                    if fpr_formats.query.get(object["fields"]["uuid"]) is not None:
                        fpr_formats.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "group": object["fields"]["group"],
                                "slug": object["fields"]["slug"],
                                "description": object["fields"]["description"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(format)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.formatversion":
                    output = object["model"] + " " + object["fields"]["description"]
                    if object["fields"]["version"] is not None:
                        output += " " + object["fields"]["version"]

                    # one of the input JSON files does not include this field
                    try:
                        replacesValue = object["fields"]["replaces"]
                    except:
                        replacesValue = None

                    # one of the input JSON files changes date format to include microseconds
                    try:
                        cleanDate = datetime.strptime(
                            object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                    except:
                        cleanupDate = object["fields"]["lastmodified"]
                        date = cleanupDate[:-5]
                        cleanDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

                    formatVersion = fpr_format_versions(
                        uuid=object["fields"]["uuid"],
                        replaces=replacesValue,
                        slug=object["fields"]["slug"],
                        description=object["fields"]["description"],
                        last_modified=cleanDate,
                        enabled=object["fields"]["enabled"],
                        access_format=object["fields"]["access_format"],
                        preservation_format=object["fields"]["preservation_format"],
                        version=object["fields"]["version"],
                        pronom_id=object["fields"]["pronom_id"],
                        format=object["fields"]["format"],
                    )

                    if (
                        fpr_format_versions.query.get(object["fields"]["uuid"])
                        is not None
                    ):
                        fpr_format_versions.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "replaces": replacesValue,
                                "slug": object["fields"]["slug"],
                                "description": object["fields"]["description"],
                                "last_modified": cleanDate,
                                "enabled": object["fields"]["enabled"],
                                "access_format": object["fields"]["access_format"],
                                "preservation_format": object["fields"][
                                    "preservation_format"
                                ],
                                "version": object["fields"]["version"],
                                "pronom_id": object["fields"]["pronom_id"],
                                "format": object["fields"]["format"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(formatVersion)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.idtool":
                    output = object["model"] + " " + object["fields"]["description"]
                    if object["fields"]["version"] is not None:
                        output += " " + object["fields"]["version"]
                    print(output)

                    idTool = fpr_id_tools(
                        uuid=object["fields"]["uuid"],
                        slug=object["fields"]["slug"],
                        version=object["fields"]["version"],
                        enabled=object["fields"]["enabled"],
                        description=object["fields"]["description"],
                    )

                    if fpr_id_tools.query.get(object["fields"]["uuid"]) is not None:
                        fpr_id_tools.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "slug": object["fields"]["slug"],
                                "version": object["fields"]["version"],
                                "enabled": object["fields"]["enabled"],
                                "description": object["fields"]["description"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(idTool)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.idcommand":
                    output = object["model"] + " " + object["fields"]["description"]

                    idCommand = fpr_id_commands(
                        uuid=object["fields"]["uuid"],
                        replaces=object["fields"]["replaces"],
                        script=object["fields"]["script"],
                        last_modified=datetime.strptime(
                            object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        enabled=object["fields"]["enabled"],
                        script_type=object["fields"]["script_type"],
                        config=object["fields"]["config"],
                        description=object["fields"]["description"],
                        id_tool=object["fields"]["tool"],
                    )

                    if fpr_id_commands.query.get(object["fields"]["uuid"]) is not None:
                        fpr_id_commands.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "replaces": object["fields"]["replaces"],
                                "script": object["fields"]["script"],
                                "last_modified": datetime.strptime(
                                    object["fields"]["lastmodified"],
                                    "%Y-%m-%dT%H:%M:%SZ",
                                ),
                                "enabled": object["fields"]["enabled"],
                                "script_type": object["fields"]["script_type"],
                                "config": object["fields"]["config"],
                                "description": object["fields"]["description"],
                                "id_tool": object["fields"]["tool"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(idCommand)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.idrule":
                    output = object["model"] + " " + object["fields"]["command_output"]

                    # one of the input JSON files changes date format to include microseconds
                    try:
                        cleanDate = datetime.strptime(
                            object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                    except:
                        cleanupDate = object["fields"]["lastmodified"]
                        date = cleanupDate[:-5]
                        cleanDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

                    idRule = fpr_id_rules(
                        uuid=object["fields"]["uuid"],
                        replaces=object["fields"]["replaces"],
                        format=object["fields"]["format"],
                        last_modified=cleanDate,
                        enabled=object["fields"]["enabled"],
                        command_output=object["fields"]["command_output"],
                        command=object["fields"]["command"],
                    )

                    if fpr_id_rules.query.get(object["fields"]["uuid"]) is not None:
                        fpr_id_rules.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "replaces": object["fields"]["replaces"],
                                "format": object["fields"]["format"],
                                "last_modified": cleanDate,
                                "enabled": object["fields"]["enabled"],
                                "command_output": object["fields"]["command_output"],
                                "command": object["fields"]["command"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(idRule)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.fptool":
                    output = object["model"] + " " + object["fields"]["description"]

                    if object["fields"]["version"] is not None:
                        output += " " + object["fields"]["version"]
                    print(output)

                    fprTool = fpr_tools(
                        uuid=object["fields"]["uuid"],
                        slug=object["fields"]["slug"],
                        version=object["fields"]["version"],
                        enabled=object["fields"]["enabled"],
                        description=object["fields"]["description"],
                    )

                    if fpr_tools.query.get(object["fields"]["uuid"]) is not None:
                        fpr_tools.query.filter_by(uuid=object["fields"]["uuid"]).update(
                            {
                                "slug": object["fields"]["slug"],
                                "version": object["fields"]["version"],
                                "enabled": object["fields"]["enabled"],
                                "description": object["fields"]["description"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(fprTool)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.fpcommand":
                    output = object["model"] + " " + object["fields"]["description"]

                    fprCommand = fpr_commands(
                        uuid=object["fields"]["uuid"],
                        replaces=object["fields"]["replaces"],
                        last_modified=datetime.strptime(
                            object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        tool=object["fields"]["tool"],
                        enabled=object["fields"]["enabled"],
                        event_detail_command=object["fields"]["event_detail_command"],
                        output_location=object["fields"]["output_location"],
                        command_usage=object["fields"]["command_usage"],
                        verification_command=object["fields"]["verification_command"],
                        command=object["fields"]["command"],
                        script_type=object["fields"]["script_type"],
                        output_format=object["fields"]["output_format"],
                        description=object["fields"]["description"],
                    )

                    if fpr_commands.query.get(object["fields"]["uuid"]) is not None:
                        fpr_commands.query.filter_by(
                            uuid=object["fields"]["uuid"]
                        ).update(
                            {
                                "replaces": object["fields"]["replaces"],
                                "last_modified": datetime.strptime(
                                    object["fields"]["lastmodified"],
                                    "%Y-%m-%dT%H:%M:%SZ",
                                ),
                                "tool": object["fields"]["tool"],
                                "enabled": object["fields"]["enabled"],
                                "event_detail_command": object["fields"][
                                    "event_detail_command"
                                ],
                                "output_location": object["fields"]["output_location"],
                                "command_usage": object["fields"]["command_usage"],
                                "verification_command": object["fields"][
                                    "verification_command"
                                ],
                                "command": object["fields"]["command"],
                                "script_type": object["fields"]["script_type"],
                                "output_format": object["fields"]["output_format"],
                                "description": object["fields"]["description"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(fprCommand)
                    db.session.commit()

            for object in jsonObjects:

                if object["model"] == "fpr.fprule":
                    output = (
                        object["model"]
                        + " "
                        + object["fields"]["purpose"]
                        + " "
                        + object["fields"]["uuid"]
                    )
                    print(output)

                    # one of the input JSON files changes date format to include microseconds
                    try:
                        cleanDate = datetime.strptime(
                            object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                    except:
                        cleanupDate = object["fields"]["lastmodified"]
                        date = cleanupDate[:-5]
                        cleanDate = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

                    fprRule = fpr_rules(
                        uuid=object["fields"]["uuid"],
                        replaces=object["fields"]["replaces"],
                        count_not_okay=object["fields"]["count_not_okay"],
                        count_attempts=object["fields"]["count_attempts"],
                        format=object["fields"]["format"],
                        last_modified=cleanDate,
                        enabled=object["fields"]["enabled"],
                        command=object["fields"]["command"],
                        purpose=object["fields"]["purpose"],
                        count_okay=object["fields"]["count_okay"],
                    )

                    if fpr_rules.query.get(object["fields"]["uuid"]) is not None:
                        fpr_rules.query.filter_by(uuid=object["fields"]["uuid"]).update(
                            {
                                "replaces": object["fields"]["replaces"],
                                "count_not_okay": object["fields"]["count_not_okay"],
                                "count_attempts": object["fields"]["count_attempts"],
                                "format": object["fields"]["format"],
                                "last_modified": cleanDate,
                                "enabled": object["fields"]["enabled"],
                                "command": object["fields"]["command"],
                                "purpose": object["fields"]["purpose"],
                                "count_okay": object["fields"]["count_okay"],
                            }
                        )
                        print("updating " + output)
                    else:
                        print("adding " + output)
                        db.session.add(fprRule)
                    db.session.commit()

    end = datetime.now()
    duration = str(end - start)[:-7]
    return duration
