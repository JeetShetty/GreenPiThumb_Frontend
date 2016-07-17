"""Temporary module to generate dummy values for GreenPiThumb.

Placeholder module to generate dummy values until we hook the GreenPiThumb web
dashboard up to the actual GreenPiThumb backend.
"""
# TODO(mtlynch): Delete this module once GreenPiThumb_Frontend is connected to
# the GreenPiThumb backend.

import datetime
import random

import pytz


def generate_values(value_name, start_value, max_delta):
    """Generate dummy a list of random dummy (timestamp, value) entries.

    Generates a list of dummy value entries (in ascending order of time) by
    starting with start_value, then changing it by max_delta each step until the
    list of dummy entries is complete.

    Args:
        value_name: The name of the value type to use in each value entry (e.g.
            "temperature".
        start_value: The base value from which to derive random values.
        max_delta: The max amount to change the value at each step.

    Returns:
        A list of random entries. For example, if the value_name was
        "temperature", the list might look like the following:

            [{'timestamp': '20160623T230615Z', 'temperature': 34.2},
             {'timestamp': '20160623T230640Z', 'temperature': 30.1},
             {'timestamp': '20160623T230705Z', 'temperature': 29.2},
             ...
             {'timestamp': '20160623T230845Z', 'temperature': 28.6}]
    """
    values = []
    timestamp = datetime.datetime.now(tz=pytz.utc)
    value = start_value
    values.insert(0, _generate_value_entry(value_name, timestamp, value))
    for _ in range(25):
        timestamp = timestamp - datetime.timedelta(seconds=25)
        value = value + random.uniform(-1 * max_delta, max_delta)
        values.insert(0, _generate_value_entry(value_name, timestamp, value))
    return values


def _generate_value_entry(value_name, timestamp, value):
    entry = {}
    entry['timestamp'] = _format_timestamp(timestamp)
    entry[value_name] = value
    return entry


def _format_timestamp(timestamp):
    return timestamp.strftime('%Y%m%dT%H:%M:%SZ')
