import datetime

import simplejson


def _encode_time(time):
    """Encodes time in YYYYMMDDTHHMMSSZ format (assumes UTC time zone)."""
    return datetime.datetime.strftime(time, '%Y%m%dT%H%M%SZ')


class Encoder(simplejson.JSONEncoder):
    """JSON encoder for GreenPiThumb objects."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return _encode_time(obj)
        return simplejson.JSONEncoder.default(self, obj)
