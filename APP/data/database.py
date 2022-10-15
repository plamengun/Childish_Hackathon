from mariadb import connect
from mariadb.connections import Connection


def _get_connection() -> Connection:
    return connect(
        user='telerik_tigers',
        password='Child.join.on.Telerik2022!',
        host='nlikyov.asuscomm.com',
        port=49495,
        database='python_hackathon_childish',
    )


def read_query(sql: str, sql_params: tuple = ()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def read_query_one(sql: str, sql_params: tuple = ()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return cursor.fetchone()


def insert_query(sql: str, sql_params: tuple = ()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params: tuple = ()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount