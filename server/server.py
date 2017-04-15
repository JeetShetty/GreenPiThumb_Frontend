#!/usr/bin/python2
"""Web server for GreenPiThumb."""

import argparse
import contextlib

import greenpithumb.greenpithumb.db_store as db_store

import app
import images


def main(args):
    with contextlib.closing(db_store.open_or_create_db(
            args.db_file)) as db_connection:
        temperature_store = db_store.TemperatureStore(db_connection)
        light_store = db_store.LightStore(db_connection)
        soil_moisture_store = db_store.SoilMoistureStore(db_connection)
        humidity_store = db_store.HumidityStore(db_connection)

        app.create(
            images.Indexer(args.image_path), temperature_store, light_store,
            soil_moisture_store, humidity_store).run('0.0.0.0', args.port)


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
