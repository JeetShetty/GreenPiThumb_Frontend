#!/usr/bin/python2
"""Web server for GreenPiThumb."""

import argparse
import contextlib

import greenpithumb.greenpithumb.db_store as db_store
import klein

import images
import json_encoder


def main(args):
    app = klein.Klein()
    encoder = json_encoder.Encoder()
    image_indexer = images.Indexer(args.image_path)
    with contextlib.closing(db_store.open_or_create_db(
            args.db_file)) as db_connection:
        temperature_store = db_store.TemperatureStore(db_connection)
        ambient_light_store = db_store.AmbientLightStore(db_connection)
        soil_moisture_store = db_store.SoilMoistureStore(db_connection)
        humidity_store = db_store.HumidityStore(db_connection)

        @app.route('/temperatureHistory.json')
        def temperature_history(request):
            return encoder.encode(temperature_store.get())

        @app.route('/lightHistory.json')
        def light_history(request):
            return encoder.encode(ambient_light_store.get())

        @app.route('/soilMoistureHistory.json')
        def soil_moisture_history(request):
            return encoder.encode(soil_moisture_store.get())

        @app.route('/ambientHumidityHistory.json')
        def ambient_humidity_history(request):
            return encoder.encode(humidity_store.get())

        @app.route('/images.json')
        def image_index(request):
            return encoder.encode(image_indexer.index())

        app.run('0.0.0.0', args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GreenPiThumb Web Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, default=8888)
    parser.add_argument(
        '-d',
        '--db_file',
        help='Path to GreenPiThumb database file',
        required=True)
    parser.add_argument(
        '-i',
        '--image_path',
        type=str,
        help='Path to folder containing GreenPiThumb images',
        required=True)
    main(parser.parse_args())
