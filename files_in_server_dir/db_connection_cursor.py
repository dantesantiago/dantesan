from contextlib import contextmanager

import mysql.connector as mariadb

from common import mdbuser, mdbpass, mdbhost, mdbport, mdb


@contextmanager
def get_db_connection(database=mdb, **kwds):
    conn = mariadb.connect(user=mdbuser, password=mdbpass,
                           host=mdbhost, port=mdbport, database=database, **kwds)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_cursor(conn, tobuffer=False, **kwargs):
    cursor = conn.cursor(buffered=tobuffer, **kwargs)
    try:
        yield cursor
    finally:
        cursor.close()
