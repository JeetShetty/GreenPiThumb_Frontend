import datetime
import json
import unittest

from dateutil import tz
import pytz

from server import record_encoder
from server.greenpithumb.greenpithumb import db_store

# Timezone offset info for EST (UTC minus 5 hours).
UTC_MINUS_5 = tz.tzoffset(None, -18000)


class RecordEncoderTest(unittest.TestCase):

    def setUp(self):
        self.encoder = record_encoder.RecordEncoder()

    def assertJsonEqual(self, expected, actual):
        json.loads(expected)
        json.loads(actual)
        self.assertDictEqual(json.loads(expected), json.loads(actual))

    def test_encodes_records_correctly(self):
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123+0000",
              "soil_moisture": 305
            }
            """.strip(),
            self.encoder.encode(
                db_store.SoilMoistureRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=pytz.utc),
                    soil_moisture=305)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123+0000",
              "ambient_light": 87.3
            }
            """.strip(),
            self.encoder.encode(
                db_store.AmbientLightRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=pytz.utc),
                    ambient_light=87.3)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123+0000",
              "humidity": 21.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.HumidityRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=pytz.utc),
                    humidity=21.5)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123+0000",
              "temperature": 21.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.TemperatureRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=pytz.utc),
                    temperature=21.5)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123+0000",
              "water_pumped": 302.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.WateringEventRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=pytz.utc),
                    water_pumped=302.5)))

    def test_encodes_non_utc_records_correctly(self):
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T150123-0500",
              "temperature": 21.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.TemperatureRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, 23, 924000, tzinfo=UTC_MINUS_5),
                    temperature=21.5)))
