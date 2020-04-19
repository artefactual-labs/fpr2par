from fpr2par import db


class fpr_format_groups(db.Model):
    uuid = db.Column(db.String(36), index=True, primary_key=True)
    slug = db.Column(db.String(255))
    description = db.Column(db.String(255))
    fprFormats = db.relationship(
        "fpr_formats", cascade="all,delete", backref="fpr_format_groups", lazy=True
    )

    def __init__(self, uuid, slug, description):
        self.uuid = uuid
        self.slug = slug
        self.description = description

    def __repr__(self):
        return "<FPR Format Groups '{}'>".format(self.description)


class fpr_formats(db.Model):
    uuid = db.Column(db.String(36), index=True, primary_key=True)
    slug = db.Column(db.String(255))
    description = db.Column(db.String(255))
    group = db.Column(
        db.String(36),
        db.ForeignKey("fpr_format_groups.uuid"),
        nullable=False,
        index=True,
    )
    fprFormatVersions = db.relationship(
        "fpr_format_versions", cascade="all,delete", backref="fpr_formats", lazy=True
    )

    def __init__(self, uuid, group, slug, description):
        self.uuid = uuid
        self.group = group
        self.slug = slug
        self.description = description

    def __repr__(self):
        return "<FPR Formats '{}'>".format(self.description)


class fpr_format_versions(db.Model):
    uuid = db.Column(db.String(36), index=True, primary_key=True)
    replaces = db.Column(db.String(36))
    slug = db.Column(db.String(255))
    description = db.Column(db.String(255))
    last_modified = db.Column(db.DateTime())
    enabled = db.Column(db.Boolean)
    access_format = db.Column(db.Boolean)
    preservation_format = db.Column(db.Boolean)
    version = db.Column(db.String(255))
    pronom_id = db.Column(db.String(255))
    format = db.Column(
        db.String(36), db.ForeignKey("fpr_formats.uuid"), nullable=False, index=True,
    )

    def __init__(
        self,
        uuid,
        replaces,
        slug,
        description,
        last_modified,
        enabled,
        access_format,
        preservation_format,
        version,
        pronom_id,
        format,
    ):
        self.uuid = uuid
        self.replaces = replaces
        self.slug = slug
        self.description = description
        self.last_modified = last_modified
        self.enabled = enabled
        self.access_format = access_format
        self.preservation_format = preservation_format
        self.version = version
        self.pronom_id = pronom_id
        self.format = format

    def __repr__(self):
        return "<FPR Format Versions '{}'>".format(self.pronom_id)


class fpr_id_tools(db.Model):
    uuid = db.Column(db.String(36), index=True, primary_key=True)
    slug = db.Column(db.String(255))
    version = db.Column(db.String(255))
    enabled = db.Column(db.Boolean)
    description = db.Column(db.String(255))
    fprIdCommands = db.relationship(
        "fpr_id_commands", cascade="all,delete", backref="fpr_id_tools", lazy=True
    )

    def __init__(
        self, uuid, slug, version, enabled, description,
    ):
        self.uuid = uuid
        self.slug = slug
        self.version = version
        self.enabled = enabled
        self.description = description

    def __repr__(self):
        return "<FPR ID Tools '{}'>".format(self.description)


class fpr_id_commands(db.Model):
    uuid = db.Column(db.String(36), index=True, primary_key=True)
    replaces = db.Column(db.String(36))
    script = db.Column(db.String(255))
    last_modified = db.Column(db.DateTime())
    enabled = db.Column(db.Boolean)
    script_type = db.Column(db.String(255))
    config = db.Column(db.String(255))
    description = db.Column(db.String(255))
    id_tool = db.Column(
        db.String(36), db.ForeignKey("fpr_id_tools.uuid"), nullable=False, index=True,
    )

    def __init__(
        self,
        uuid,
        replaces,
        script,
        last_modified,
        enabled,
        script_type,
        config,
        description,
        id_tool,
    ):
        self.uuid = uuid
        self.replaces = replaces
        self.script = script
        self.last_modified = last_modified
        self.enabled = enabled
        self.script_type = script_type
        self.config = config
        self.description = description
        self.id_tool = id_tool

    def __repr__(self):
        return "<FPR ID Commands '{}'>".format(self.description)
