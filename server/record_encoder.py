import datetime

import simplejson


def _encode_time(time):
    """Encodes time in YYYYMMDDTHHMMSS+Z format."""
    return datetime.datetime.strftime(time, '%Y%m%dT%H%M%S%z')


class RecordEncoder(simplejson.JSONEncoder):
    """JSON encoder for GreenPiThumb DB records."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return _encode_time(obj)
        return simplejson.JSONEncoder.default(self, obj)
