from fpr2par import db
from .models import (
    fpr_formats,
    fpr_format_groups,
    fpr_format_versions,
    fpr_id_tools,
    fpr_id_commands,
)
import json
import datetime


def adddata():

    with open("sourceJSON/initial_data.json", "r") as jsonFile:
        data = jsonFile.read()

    jsonObjects = json.loads(data)

    for object in jsonObjects:

        if object["model"] == "fpr.formatgroup":
            print(object["model"] + " " + object["fields"]["description"])

            formatGroup = fpr_format_groups(
                uuid=object["fields"]["uuid"],
                slug=object["fields"]["slug"],
                description=object["fields"]["description"],
            )

            db.session.add(formatGroup)
            db.session.commit()

    for object in jsonObjects:

        if object["model"] == "fpr.format":
            print(object["model"] + " " + object["fields"]["description"])

            format = fpr_formats(
                uuid=object["fields"]["uuid"],
                group=object["fields"]["group"],
                slug=object["fields"]["slug"],
                description=object["fields"]["description"],
            )

            db.session.add(format)
            db.session.commit()

    for object in jsonObjects:

        if object["model"] == "fpr.formatversion":
            output = object["model"] + " " + object["fields"]["description"]
            if object["fields"]["version"] is not None:
                output += " " + object["fields"]["version"]
            print(output)

            formatVersion = fpr_format_versions(
                uuid=object["fields"]["uuid"],
                replaces=object["fields"]["replaces"],
                slug=object["fields"]["slug"],
                description=object["fields"]["description"],
                last_modified=datetime.datetime.strptime(
                    object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                enabled=object["fields"]["enabled"],
                access_format=object["fields"]["access_format"],
                preservation_format=object["fields"]["preservation_format"],
                version=object["fields"]["version"],
                pronom_id=object["fields"]["pronom_id"],
                format=object["fields"]["format"],
            )

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

            db.session.add(idTool)
            db.session.commit()

    for object in jsonObjects:

        if object["model"] == "fpr.idcommand":
            output = object["model"] + " " + object["fields"]["description"]
            print(output)

            idCommand = fpr_id_commands(
                uuid=object["fields"]["uuid"],
                replaces=object["fields"]["replaces"],
                script=object["fields"]["script"],
                last_modified=datetime.datetime.strptime(
                    object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                enabled=object["fields"]["enabled"],
                script_type=object["fields"]["script_type"],
                config=object["fields"]["config"],
                description=object["fields"]["description"],
                id_tool=object["fields"]["tool"],
            )

            db.session.add(idCommand)
            db.session.commit()

    return ()
