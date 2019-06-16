from flask import jsonify


def create_rates_handler(
    date_from_param,
    date_to_param,
    orig_ports_param,
    dest_ports_param,
    fetch_rates
):
    def handle(request, min_sample=0):
        params = request.args
        date_from = date_from_param(params)
        date_to = date_to_param(params)
        orig_ports = orig_ports_param(params)
        dest_ports = dest_ports_param(params)

        rates = fetch_rates(
            date_from,
            date_to,
            orig_ports,
            dest_ports,
            min_sample
        )

        return jsonify(rates)

    return handle
