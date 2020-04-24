# -*- coding: utf-8 -*-

def _parse_offset_limit(request):
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=None, type=int)
    if limit is not None:
        limit = offset + limit
    return offset, limit
