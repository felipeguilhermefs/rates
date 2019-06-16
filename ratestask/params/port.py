import re

from ..api_exception import InvalidQueryParam

PORT_PATTERN = re.compile(r'^[A-Z]{5}$')


def port_param(query_param):
    def getter(params):
        if query_param not in params:
            raise InvalidQueryParam(f'param \'{query_param}\' is required')

        param = params[query_param]

        if PORT_PATTERN.match(param):
            return param

        raise InvalidQueryParam(f'param \'{query_param}\' must be a port code')

    return getter
