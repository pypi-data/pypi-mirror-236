""" starts the server """

from psycopg2 import connect, Error as PGError  # type: ignore
from teamhack_db.conf import config  # type: ignore
from teamhack_db.sql import create_table  # type: ignore
from teamhack_rest.server import start_server

if __name__ == '__main__':
    params = config()
    conn = connect(**params)

    try:
        create_table(conn)
        conn.commit()
    except PGError as e:
        print(f"Error: {e}")
        conn.rollback()
        raise e

    start_server(conn)
