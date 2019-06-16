import requests


def create_fetch_exchange_rates(api_key):

    # Maybe this could be cached
    def fetch_exchange_rates():
        response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={api_key}&base=USD')
        if response.ok:
            return response.json()['rates']
        else:
            # Would be nice to have a fallback strategy
            return dict()

    return fetch_exchange_rates
