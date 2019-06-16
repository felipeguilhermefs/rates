from datetime import datetime

from ..api_exception import InvalidQueryParam

def iso_date_param(query_param):
    def getter(params):
        if query_param not in params:
            raise InvalidQueryParam(f'param \'{query_param}\' is required')

        param = params[query_param]

        try:
            return datetime.strptime(param, '%Y-%m-%d').date()
        except ValueError:
            raise InvalidQueryParam(f'query param \'{query_param}\' must have "yyyy-mm-dd" format')

    return getter
