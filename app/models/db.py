import sqlite3
import os
from flask import current_app

def get_connection(db_path=None):
    if db_path is None:
        db_path = current_app.config['DB_PATH']
    return sqlite3.connect(db_path)

def init_db(db_path, schema_path, data_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if os.path.exists(db_path):
        os.remove(db_path)

    conn = get_connection(db_path)

    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

    with open(data_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()
