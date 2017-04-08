import datetime
import json
import unittest

import pytz

from server import json_encoder
from server.greenpithumb.greenpithumb import db_store


class JSONEncoderTest(unittest.TestCase):

    def setUp(self):
        self.encoder = json_encoder.Encoder()

    def assertJsonEqual(self, expected, actual):
        json.loads(expected)
        json.loads(actual)
        self.assertDictEqual(json.loads(expected), json.loads(actual))

    def test_encodes_records_correctly(self):
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T1501Z",
              "soil_moisture": 305
            }
            """.strip(),
            self.encoder.encode(
                db_store.SoilMoistureRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, tzinfo=pytz.utc),
                    soil_moisture=305)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T1501Z",
              "ambient_light": 87.3
            }
            """.strip(),
            self.encoder.encode(
                db_store.AmbientLightRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, tzinfo=pytz.utc),
                    ambient_light=87.3)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T1501Z",
              "humidity": 21.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.HumidityRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, tzinfo=pytz.utc),
                    humidity=21.5)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T1501Z",
              "temperature": 21.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.TemperatureRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, tzinfo=pytz.utc),
                    temperature=21.5)))
        self.assertJsonEqual(
            """
            {
              "timestamp": "20170319T1501Z",
              "water_pumped": 302.5
            }
            """.strip(),
            self.encoder.encode(
                db_store.WateringEventRecord(
                    timestamp=datetime.datetime(
                        2017, 3, 19, 15, 1, tzinfo=pytz.utc),
                    water_pumped=302.5)))
