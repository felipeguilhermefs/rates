from psycopg2 import pool


def create_datasource(config):
    # We create a pool so we go easier on the database
    # and we can handle request faster as well
    connection_pool = pool.ThreadedConnectionPool(
        minconn=config['PG_POOL_MIN'],
        maxconn=config['PG_POOL_MAX'],
        user=config['PG_USER'],
        password=config['PG_PASS'],
        host=config['PG_HOST'],
        port=config['PG_PORT'],
        database=config['PG_DB']
    )

    def read_datasource(query, row_mapper):
        # we abstract connection handling as managing a pool and cursor
        # do not need to be done at every interaction with the datasource
        conn = connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row_mapper(record) for record in cur]
        finally:
            connection_pool.putconn(conn)

    def write_datasource(inserts):
        # like read, we abstract connection handling
        conn = connection_pool.getconn()
        try:
            with conn.cursor() as cur:
                for insert in inserts:
                    cur.execute(insert)
                conn.commit()

        except Exception:
            conn.rollback()
        finally:
            connection_pool.putconn(conn)

    return read_datasource, write_datasource
