import flask

import json_encoder


def create(image_indexer, temperature_store, light_store, soil_moisture_store,
           humidity_store):
    """Creates a new GreenPiThumb flask app.

    Creates a GreenPiThumb app capable of servicing requests to the GreenPiThumb
    frontend's dynamic resources.

    Args:
        image_indexer: Interface for indexing GreenPiThumb images.
        temperature_store: Interface for retrieving temperature records.
        light_store: Interface for retrieving light records.
        soil_moisture_store: Interface for retrieving soil moisture records.
        humidity_store: Interface for retrieving humidity records.

    Returns:
        A Flask app that can serve HTTP requests.
    """
    app = flask.Flask(__name__)
    encoder = json_encoder.Encoder()

    @app.route('/temperatureHistory.json')
    def temperature_history():
        return encoder.encode(temperature_store.get())

    @app.route('/lightHistory.json')
    def light_history():
        return encoder.encode(light_store.get())

    @app.route('/soilMoistureHistory.json')
    def soil_moisture_history():
        return encoder.encode(soil_moisture_store.get())

    @app.route('/humidityHistory.json')
    def humidity_history():
        return encoder.encode(humidity_store.get())

    @app.route('/images.json')
    def image_index():
        return encoder.encode(image_indexer.index())

    return app
