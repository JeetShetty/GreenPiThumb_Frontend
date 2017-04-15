import datetime
import json
import unittest

import mock
import pytz
import server.greenpithumb.greenpithumb.db_store as db_store

from server import app
from server import images


class AppTest(unittest.TestCase):

    def assertJsonEqual(self, expected, actual):
        json.loads(expected)
        json.loads(actual)
        self.assertEqual(json.loads(expected), json.loads(actual))

    def test_temperature_history_empty_db(self):
        mock_temperature_store = mock.Mock(spec_set=db_store.TemperatureStore)
        mock_temperature_store.get.return_value = []
        app_client = app.create(
            image_indexer=None,
            temperature_store=mock_temperature_store,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/temperatureHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("[]", response.data)

    def test_temperature_history_non_empty_db(self):
        mock_temperature_store = mock.Mock(spec_set=db_store.TemperatureStore)
        mock_temperature_store.get.return_value = [
            db_store.TemperatureRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 10, 51, 0, tzinfo=pytz.utc),
                temperature=57.3),
            db_store.TemperatureRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 11, 39, 0, tzinfo=pytz.utc),
                temperature=68.2),
        ]
        app_client = app.create(
            image_indexer=None,
            temperature_store=mock_temperature_store,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/temperatureHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("""
            [
                {
                    "timestamp": "20170415T1051Z",
                    "temperature": 57.3
                },
                {
                    "timestamp": "20170415T1139Z",
                    "temperature": 68.2
                }
            ]
            """, response.data)

    def test_light_history_empty_db(self):
        mock_light_store = mock.Mock(spec_set=db_store.LightStore)
        mock_light_store.get.return_value = []
        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=mock_light_store,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/lightHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("[]", response.data)

    def test_light_history_non_empty_db(self):
        mock_light_store = mock.Mock(spec_set=db_store.LightStore)
        mock_light_store.get.return_value = [
            db_store.LightRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 10, 51, 0, tzinfo=pytz.utc),
                light=57.3),
            db_store.LightRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 11, 39, 0, tzinfo=pytz.utc),
                light=68.2),
        ]
        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=mock_light_store,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/lightHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("""
            [
                {
                    "timestamp": "20170415T1051Z",
                    "light": 57.3
                },
                {
                    "timestamp": "20170415T1139Z",
                    "light": 68.2
                }
            ]
            """, response.data)

    def test_soil_moisture_history_empty_db(self):
        mock_soil_moisture_store = mock.Mock(spec_set=db_store.SoilMoistureStore)
        mock_soil_moisture_store.get.return_value = []

        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=mock_soil_moisture_store,
            humidity_store=None).test_client(self)
        response = app_client.get('/soilMoistureHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("[]", response.data)

    def test_soil_moisture_history_non_empty_db(self):
        mock_soil_moisture_store = mock.Mock(spec_set=db_store.SoilMoistureStore)
        mock_soil_moisture_store.get.return_value = [
            db_store.SoilMoistureRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 10, 51, 0, tzinfo=pytz.utc),
                soil_moisture=57.3),
            db_store.SoilMoistureRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 11, 39, 0, tzinfo=pytz.utc),
                soil_moisture=68.2),
        ]
        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=mock_soil_moisture_store,
            humidity_store=None).test_client(self)
        response = app_client.get('/soilMoistureHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("""
            [
                {
                    "timestamp": "20170415T1051Z",
                    "soil_moisture": 57.3
                },
                {
                    "timestamp": "20170415T1139Z",
                    "soil_moisture": 68.2
                }
            ]
            """, response.data)

    def test_humidity_history_empty_db(self):
        mock_humidity_store = mock.Mock(spec_set=db_store.HumidityStore)
        mock_humidity_store.get.return_value = []
        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=mock_humidity_store).test_client(self)
        response = app_client.get('/humidityHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("[]", response.data)

    def test_humidity_history_non_empty_db(self):
        mock_humidity_store = mock.Mock(spec_set=db_store.HumidityStore)
        mock_humidity_store.get.return_value = [
            db_store.HumidityRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 10, 51, 0, tzinfo=pytz.utc),
                humidity=57.3),
            db_store.HumidityRecord(
                timestamp=datetime.datetime(
                    2017, 4, 15, 11, 39, 0, tzinfo=pytz.utc),
                humidity=68.2),
        ]
        app_client = app.create(
            image_indexer=None,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=mock_humidity_store).test_client(self)
        response = app_client.get('/humidityHistory.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("""
            [
                {
                    "timestamp": "20170415T1051Z",
                    "humidity": 57.3
                },
                {
                    "timestamp": "20170415T1139Z",
                    "humidity": 68.2
                }
            ]
            """, response.data)

    def test_images_empty_index(self):
        mock_image_indexer = mock.Mock(spec_set=images.Indexer)
        mock_image_indexer.index.return_value = []
        app_client = app.create(
            image_indexer=mock_image_indexer,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/images.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("[]", response.data)

    def test_images_non_empty_index(self):
        mock_image_indexer = mock.Mock(spec_set=images.Indexer)
        mock_image_indexer.index.return_value = [
            {
                'timestamp': datetime.datetime(
                    2017, 4, 1, 18, 51, 0, tzinfo=pytz.utc),
                'filename': '2017-04-01T1851Z.jpg',
            },
            {
                'timestamp': datetime.datetime(
                    2017, 4, 1, 18, 53, 0, tzinfo=pytz.utc),
                'filename': '2017-04-01T1853Z.jpg',
            },
        ]
        app_client = app.create(
            image_indexer=mock_image_indexer,
            temperature_store=None,
            light_store=None,
            soil_moisture_store=None,
            humidity_store=None).test_client(self)
        response = app_client.get('/images.json')
        self.assertEqual(200, response.status_code)
        self.assertJsonEqual("""
            [
              {
                "timestamp": "20170401T1851Z",
                "filename": "2017-04-01T1851Z.jpg"
              },
              {
                "timestamp": "20170401T1853Z",
                "filename": "2017-04-01T1853Z.jpg"
              }
            ]
            """, response.data)
