from flask import Flask, jsonify, request

from .api_exception import InvalidQueryParam, InvalidContentType
from .commands import create_insert_prices
from .datasource import create_datasource
from .handlers import create_prices_handler, create_rates_handler
from .params import iso_date_param, ports_param, currency_param
from .queries import create_fetch_exchange_rates, create_fetch_ports, create_fetch_rates


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py', silent=True)

    read_datasource, write_datasource = create_datasource(app.config)

    fetch_ports = create_fetch_ports(read_datasource)
    fetch_rates = create_fetch_rates(read_datasource)
    fetch_exchange_rates = create_fetch_exchange_rates(app.config['EX_RT_API_KEY'])
    insert_prices = create_insert_prices(write_datasource)

    date_from_param = iso_date_param('date_from')
    date_to_param = iso_date_param('date_to')
    orig_ports_param = ports_param('origin', fetch_ports)
    dest_ports_param = ports_param('destination', fetch_ports)
    price_param = currency_param('price', 'currency', fetch_exchange_rates)

    rates_handler = create_rates_handler(
        date_from_param,
        date_to_param,
        orig_ports_param,
        dest_ports_param,
        fetch_rates
    )

    prices_handler = create_prices_handler(
        date_from_param,
        date_to_param,
        orig_ports_param,
        dest_ports_param,
        price_param,
        insert_prices
    )

    @app.route('/rates')
    def get_rates():
        return rates_handler(request)

    @app.route('/rates_null')
    def get_rates_null():
        return rates_handler(request, min_sample=3)

    @app.route('/prices', methods=['POST'])
    def prices():
        return prices_handler(request)

    @app.errorhandler(InvalidQueryParam)
    def handle_invalid_query_param(error):
        response = jsonify({'message': error.message})
        response.status_code = 400
        return response

    @app.errorhandler(InvalidContentType)
    def handle_invalid_content_type(error):
        response = jsonify({'message': error.message})
        response.status_code = 400
        return response

    return app
