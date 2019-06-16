from datetime import timedelta
from flask import jsonify

from ..api_exception import InvalidContentType


def create_prices_handler(
    date_from_param,
    date_to_param,
    orig_ports_param,
    dest_ports_param,
    price_param,
    insert_prices
):

    def date_range(date_from, date_to):
        days_between = (date_to - date_from).days
        for i in range(days_between+1):
            yield date_from + timedelta(i)

    def handle(request):
        data = request.json if request.is_json else request.form
        if data is None:
            raise InvalidContentType(f'body content should be json or form')

        date_from = date_from_param(data)
        date_to = date_to_param(data)

        # Maybe should limit just to port to port
        orig_ports = orig_ports_param(data)
        dest_ports = dest_ports_param(data)

        price = price_param(data)

        # Maybe should have a max period
        period = date_range(date_from, date_to)

        new_records = (
            (orig_port, dest_port, day, price)
            for day in period
            for dest_port in dest_ports
            for orig_port in orig_ports
        )

        insert_prices(new_records)

        return jsonify({'message': 'OK'})

    return handle
