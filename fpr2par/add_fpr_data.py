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

    for object in jsonObjects:

        if object["model"] == "fpr.idrule":
            output = object["model"] + " " + object["fields"]["command_output"]
            print(output)

            idRule = fpr_id_rules(
                uuid=object["fields"]["uuid"],
                replaces=object["fields"]["replaces"],
                format=object["fields"]["format"],
                last_modified=datetime.datetime.strptime(
                    object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                enabled=object["fields"]["enabled"],
                command_output=object["fields"]["command_output"],
                command=object["fields"]["command"],
            )

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

            db.session.add(fprTool)
            db.session.commit()

    for object in jsonObjects:

        if object["model"] == "fpr.fpcommand":
            output = object["model"] + " " + object["fields"]["description"]
            print(output)

            fprCommand = fpr_commands(
                uuid=object["fields"]["uuid"],
                replaces=object["fields"]["replaces"],
                last_modified=datetime.datetime.strptime(
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

            fprRule = fpr_rules(
                uuid=object["fields"]["uuid"],
                replaces=object["fields"]["replaces"],
                count_not_okay=object["fields"]["count_not_okay"],
                count_attempts=object["fields"]["count_attempts"],
                format=object["fields"]["format"],
                last_modified=datetime.datetime.strptime(
                    object["fields"]["lastmodified"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                enabled=object["fields"]["enabled"],
                command=object["fields"]["command"],
                purpose=object["fields"]["purpose"],
                count_okay=object["fields"]["count_okay"],
            )

            db.session.add(fprRule)
            db.session.commit()

    return ()
