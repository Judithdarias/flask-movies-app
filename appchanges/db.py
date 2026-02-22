import sqlite3

DB_PATH = "data/movies.sqlite"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comentarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pelicula TEXT NOT NULL,
        persona TEXT NOT NULL,
        comentario TEXT NOT NULL,
        fecha TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()