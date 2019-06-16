import re

from ..api_exception import InvalidQueryParam

PORT_PATTERN = re.compile(r'^[A-Z]{5}$')
REGION_PATTERN = re.compile(r'^\w+$')


def ports_param(query_param, fetch_ports):
    def getter(params):
        if query_param not in params:
            raise InvalidQueryParam(f'param \'{query_param}\' is required')

        param = params[query_param]

        if PORT_PATTERN.match(param):
            return [param]

        # Although it does not ensure it is a valid region, it sanitizes the query param
        if not REGION_PATTERN.match(param):
            raise InvalidQueryParam(
                f'param \'{query_param}\' must be a port code or a region')

        ports = fetch_ports(param)
        if not ports:
            raise InvalidQueryParam(
                f'param \'{query_param}\' does not have ports associated')

        return ports

    return getter
