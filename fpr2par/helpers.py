# -*- coding: utf-8 -*-
from datetime import datetime


def _parse_offset_limit(request):
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=None, type=int)
    if limit is not None:
        limit = offset + limit
    return offset, limit


def _split_ms(date_string):
    return str(date_string).split(".")[0]


def _get_date(date_string, default):
    try:
        return datetime.strptime(_split_ms(date_string), DATE_FORMAT_FULL)
    except ValueError:
        pass
    try:
        return datetime.strptime(_split_ms(date_string), DATE_FORMAT_PARTIAL)
    except ValueError:
        return default


DATE_FORMAT_FULL = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_PARTIAL = "%Y-%m-%d"


def _parse_filter_dates(request):
    default_after = datetime.strptime("1970-01-01 00:00:00", DATE_FORMAT_FULL)
    default_before = datetime.strptime(
        _split_ms(datetime.now(tz=None)), DATE_FORMAT_FULL
    )

    after_date = request.args.get("modified-after", default=None, type=str)
    before_date = request.args.get("modified-before", default=None, type=str)

    before_date = _get_date(before_date, default_before)
    after_date = _get_date(after_date, default_after)

    return before_date, after_date
