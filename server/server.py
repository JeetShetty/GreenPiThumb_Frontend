#!/usr/bin/python2
"""Web server for GreenPiThumb."""

import argparse
import json

import klein
from twisted.web.static import File

import dummy_values


def main(args):
    app = klein.Klein()

    @app.route('/temperatureHistory.json')
    def temperature_history(request):
        # TODO(mtlynch): Replace this with the real temperature history.
        return json.dumps(dummy_values.generate_values('temperature', 34.2,
                                                       5.0))

    # TODO(mtlynch): It might make more sense to bring nginx into this stack so
    # that nginx handles static files and Python just handles things that have
    # to be calculated on the fly. This is okay for now, though.
    @app.route('/dashboard')
    def home(request):
        return File('./static/dashboard.html')

    @app.route('/static/', branch=True)
    def static(request):
        return File('./static')

    app.run('0.0.0.0', args.port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GreenPiThumb Web Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, default=8888)
    main(parser.parse_args())
