def create_fetch_rates(datasource):

    def build_ports_clause(ports):
        quoted = map(lambda p: f"'{p}'", ports)
        return ','.join(quoted)

    def build_query(date_from, date_to, orig_ports, dest_ports):
        orig_clause = build_ports_clause(orig_ports)
        dest_clause = build_ports_clause(dest_ports)

        return f"""
    SELECT day, AVG(price) average_price, COUNT(*) total
    FROM prices
    WHERE
        day BETWEEN '{date_from}' AND '{date_to}'
        AND orig_code IN ({orig_clause})
        AND dest_code IN ({dest_clause})
    GROUP BY day
    ORDER BY day;
    """

    def build_rate(record, min_sample):
        day = record[0]
        average = record[1]
        total = record[2]
        return {
            'day': day,
            'average_price': average if total >= min_sample else None
        }

    def fetch_rates(date_from, date_to, orig_ports, dest_ports, min_sample=0):
        query = build_query(date_from, date_to, orig_ports, dest_ports)
        return datasource(query, row_mapper=lambda r: build_rate(r, min_sample))

    return fetch_rates