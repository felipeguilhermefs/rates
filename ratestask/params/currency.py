import re

from ..api_exception import InvalidQueryParam

CURRENCY_PATTERN = re.compile(r'^[A-Z]{3}$')


def currency_param(price_param, currency_param, fetch_exchange_rates):

    def getter(params):
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
