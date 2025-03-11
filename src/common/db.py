import sqlite3


def _connect(db_path):
    # db_path = config.DB_PATH
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    return conn, cur


def execute_select(query, path, data=None):
    conn, cur = _connect(path)
    cur.execute(query, data)
    result = cur.fetchall()
    conn.close()

    return result


def execute(query, path, data=None):
    conn, cur = _connect(path)
    if data is None:
        cur.execute(query)
    else:
        cur.execute(query, data)
    conn.commit()
    conn.close()



