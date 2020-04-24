# -*- coding: utf-8 -*-
import json
import os
import uuid
from datetime import datetime

import pytest
from jsonschema import ValidationError, validate

from fpr2par import app, create_fpr2par_database, db, models, views


def init_db():
    """Feed the test database with some initial data to test against."""
    format_group_one = models.fpr_format_groups(
        uuid=str(uuid.uuid4()),
        slug="group_slug_one",
        description="format_group_description_one",
    )
    format_group_two = models.fpr_format_groups(
        uuid=str(uuid.uuid4()),
        slug="group_slug_two",
        description="format_group_description_two",
    )
    file_format_1 = models.fpr_formats(
        uuid=str(uuid.uuid4()),
        group=format_group_one.uuid,
        slug="test_slug one",
        description="format_description_one",
    )
    file_format_2 = models.fpr_formats(
        uuid=str(uuid.uuid4()),
        group=format_group_two.uuid,
        slug="test_slug two",
        description="format_description_two",
    )
    date_ = datetime.strptime("1970-01-01T00:00:01", "%Y-%m-%dT%H:%M:%S")
    format_version_1 = models.fpr_format_versions(
        uuid=str(uuid.uuid4()),
        replaces="",
        slug="format_version_slug_one",
        description="format_version_description_one",
        last_modified=date_,
        enabled=True,
        access_format=False,
        preservation_format=False,
        version="0.0.0",
        pronom_id="fmt/xyz-1",
        format=file_format_1.uuid,
    )
    format_version_2 = models.fpr_format_versions(
        uuid=str(uuid.uuid4()),
        replaces="",
        slug="format_version_slug_two",
        description="format_version_description_two",
        last_modified=date_,
        enabled=True,
        access_format=False,
        preservation_format=False,
        version="0.0.0",
        pronom_id="fmt/xyz-2",
        format=file_format_2.uuid,
    )
    db.session.add(format_group_one)
    db.session.add(format_group_two)
    db.session.add(file_format_1)
    db.session.add(file_format_2)
    db.session.add(format_version_1)
    db.session.add(format_version_2)
    db.session.commit()


@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.test_request_context() as client:
        with app.app_context():
            create_fpr2par_database.createdbase()
            init_db()
        yield client
    db = None


def pretty_validate(json_resp, schema):
    """Make the output of the validation as friendly as possible."""
    try:
        validate(json_resp, schema=schema)
    except ValidationError as err:
        assert False, err


def test_file_formats(client):
    """Test the database configuration and creation."""
    formats = views.fileformats()
    # TODO: Workflow needed to update schema dynamically-ish, e.g. when updated
    # pull in the changes.
    format_schema_path = os.path.join("schema", "types.json")
    json_resp = json.loads(formats.response[0])
    with open(format_schema_path) as json_file:
        schema = json.load(json_file)
        pretty_validate(json_resp, schema=schema)
    assert (
        len(json_resp["fileFormats"]) == 2
    ), "Expecting more than one format to iterate over"
    for format_entry in json_resp["fileFormats"]:
        format_schema_path = os.path.join("schema", "format.json")
        with open(format_schema_path) as json_file:
            schema = json.load(json_file)
            pretty_validate(format_entry, schema=schema)


def test_file_format(client):
    """Test the database configuration and creation."""
    uuids = [formats.uuid for formats in models.fpr_format_versions.query.all()]
    # TODO: Workflow needed to update schema dynamically-ish, e.g. when updated
    # pull in the changes.
    format_schema_path = os.path.join("schema", "format.json")
    with open(format_schema_path) as json_file:
        schema = json.load(json_file)
        # Validate our first response.
        formats = views.fileformat(uuids[0])
        json_resp = json.loads(formats.response[0])
        pretty_validate(json_resp, schema=schema)
        # Validate our second response.
        formats = views.fileformat(uuids[0])
        json_resp = json.loads(formats.response[0])
        try:
            pretty_validate(json_resp, schema=schema)
        except ValidationError as err:
            raise ValidationError(err)
