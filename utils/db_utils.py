import sqlite3


def fetch_data(query, params=()):
    conn = sqlite3.connect('database/ecommerce.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data


def execute_query(query, params=()):
    conn = sqlite3.connect('database/ecommerce.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
