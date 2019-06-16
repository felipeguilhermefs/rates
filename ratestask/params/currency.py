import re

from ..api_exception import InvalidQueryParam

CURRENCY_PATTERN = re.compile(r'^[A-Z]{3}$')


def currency_param(price_param, currency_param, fetch_exchange_rates):

    def to_int(params, param):
        try:
            return int(params[param])
        except ValueError:
            raise InvalidQueryParam(f'param \'{param}\' must be an integer')

    def getter(params):
        if price_param not in params:
            raise InvalidQueryParam(f'param \'{price_param}\' is required')

        price = to_int(params, price_param)

        if currency_param not in params:
            return price

        currency = params[currency_param]

        if currency == 'USD':
            return price

        if not CURRENCY_PATTERN.match(currency):
            raise InvalidQueryParam(
                f'param \'{currency_param}\' must 3 digit currency id')

        exchange_rates = fetch_exchange_rates()
        if currency not in exchange_rates:
            raise InvalidQueryParam(
                f'param \'{currency_param}\' is not a currency or could not be found')

        return price / exchange_rates[currency]

    return getter
