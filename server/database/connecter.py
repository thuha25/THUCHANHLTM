import sqlite3

DB_URL = 'server/database/database.db'

def get_connection():
    return sqlite3.connect(DB_URL)

def get_cursor():
    conn = sqlite3.connect(DB_URL)
    return conn.cursor()