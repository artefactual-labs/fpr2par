# -*- coding: utf-8 -*-
from datetime import datetime


def _parse_offset_limit(request):
    """Parse offset and limit values from a given Flask request and return
    a tuple containing both.
    """
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=None, type=int)
    if limit is not None:
        limit = offset + limit
    return offset, limit


def _split_ms(date_string):
    """Remove microseconds from the given date string."""
    return str(date_string).split(".")[0]


def _get_date(date_string, default):
    """Return a date object from a given string."""
    try:
        return datetime.strptime(_split_ms(date_string), DATE_FORMAT_FULL)
    except ValueError:
        pass
    try:
        return datetime.strptime(_split_ms(date_string), DATE_FORMAT_PARTIAL)
    except ValueError:
        return default


# Date formats that can be sent via PAR requests.
DATE_FORMAT_FULL = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_PARTIAL = "%Y-%m-%d"

# Filter headers that can be sent via PAR requests.
GUID_HEADER = "guid"
FILE_FORMAT_HEADER = "file-format"
PRESERVATION_ACT_HEADER = "preservation-action-type"


def _parse_filter_dates(request):
    """Parses dates requested by the API caller and returns a before and after
    date depending on what information we have available, e.g. a blank after
    date will always return 1970-01-01.
    """
    default_after = datetime.strptime("1970-01-01 00:00:00", DATE_FORMAT_FULL)
    default_before = datetime.strptime(
        _split_ms(datetime.now(tz=None)), DATE_FORMAT_FULL
    )

    after_date = request.args.get("modified-after", default=None, type=str)
    before_date = request.args.get("modified-before", default=None, type=str)

    before_date = _get_date(before_date, default_before)
    after_date = _get_date(after_date, default_after)

    return before_date, after_date


def _get_filter_list(filter_header):
    """Returns a cleaned list from the provided header string."""
    if filter_header is None:
        return []
    filters = [item.strip() for item in filter_header.rstrip(",").split(",")]
    return filters


def _parse_filter_headers(request):
    """Accesses request headers individually and cleans them up to be used
    by the caller.

    TODO: Validate these values so that they're conform to specific regex.
    """
    guid_header = _get_filter_list(request.headers.get(GUID_HEADER))
    file_format_header = _get_filter_list(request.headers.get(FILE_FORMAT_HEADER))
    preservation_act_header = _get_filter_list(
        request.headers.get(PRESERVATION_ACT_HEADER)
    )
    return {
        GUID_HEADER: guid_header,
        FILE_FORMAT_HEADER: file_format_header,
        PRESERVATION_ACT_HEADER: preservation_act_header,
    }
