from flask import Flask, jsonify, request

from .api_exception import InvalidQueryParam
from .params import iso_date_param, ports_param


def create_app():
    app = Flask(__name__)

    def fetch_ports(_):
        return ['TESTS', 'TESTX']

    date_from_param = iso_date_param('date_from')
    date_to_param = iso_date_param('date_to')
    orig_ports_param = ports_param('origin', fetch_ports)
    dest_ports_param = ports_param('destination', fetch_ports)

    @app.route('/rates')
    def get_rates():
        response = {
            'date_from': date_from_param(request.args),
            'date_to': date_to_param(request.args),
            'orig_ports': orig_ports_param(request.args),
            'dest_ports': dest_ports_param(request.args)
        }
        return jsonify(response)

    @app.errorhandler(InvalidQueryParam)
    def handle_invalid_query_param(error):
        response = jsonify({'message': error.message})
        response.status_code = 400
        return response

    return app
