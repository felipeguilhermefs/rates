def create_fetch_rates(datasource):

    def build_ports_clause(ports):
        quoted = map(lambda p: f"'{p}'", ports)
        return ','.join(quoted)

    def build_query(date_from, date_to, orig_ports, dest_ports):
        orig_clause = build_ports_clause(orig_ports)
        dest_clause = build_ports_clause(dest_ports)

        return f"""
    SELECT day, AVG(price) average_price
    FROM prices
    WHERE
        day BETWEEN '{date_from}' AND '{date_to}'
        AND orig_code IN ({orig_clause})
        AND dest_code IN ({dest_clause})
    GROUP BY day
    ORDER BY day;
    """

    def build_rate(record):
        return {
            'day': record[0],
            'average_price': record[1]
        }

    def fetch_rates(date_from, date_to, orig_ports, dest_ports):
        query = build_query(date_from, date_to, orig_ports, dest_ports)
        return datasource(query, row_mapper=build_rate)

    return fetch_rates
