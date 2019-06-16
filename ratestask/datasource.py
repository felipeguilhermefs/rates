from psycopg2 import pool


def create_pool(
    user,
    password,
    port,
    host,
    database,
    min_conn=1,
    max_conn=10
):
    # We create a pool so we go easier on the database
    # and we can handle request faster as well
    return pool.ThreadedConnectionPool(
        minconn=min_conn,
        maxconn=max_conn,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database
    )

def create_read_datasource(pool):

    def execute(query, row_mapper):
        # we abstract connection handling as managing a pool and cursor 
        # do not need to be done at every interaction with the datasource
        conn = pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                return [row_mapper(record) for record in cur]
        finally:
            pool.putconn(conn)

    return execute

def create_write_datasource(pool):

    def execute(inserts):
        # like read, we abstract connection handling
        conn = pool.getconn()
        try:
            with conn.cursor() as cur:
                for insert in inserts:
                    cur.execute(insert)
                conn.commit()

        except Exception:
            conn.rollback()
        finally:
            pool.putconn(conn)

    return execute
