def create_fetch_ports(datasource):

    def build_query(region):
        return f"""
        WITH RECURSIVE region_groups(slug) AS (
            SELECT slug
            FROM regions
            WHERE slug = '{region}'
            UNION ALL
            SELECT regions.slug
            FROM regions, region_groups
            WHERE regions.parent_slug = region_groups.slug
        )
        SELECT ports.code
        FROM ports
        JOIN region_groups ON region_groups.slug = ports.parent_slug;
        """

    # Since ports and regions are not created frequently, this function can be
    # easily cached to improve performance
    def fetch_ports(region):
        query = build_query(region)
        return datasource(query, row_mapper=lambda row: row[0])

    return fetch_ports
