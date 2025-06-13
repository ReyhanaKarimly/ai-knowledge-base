import sqlite3

DB_PATH = "data.db"
conn = None

def init_db():
    global conn
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id TEXT PRIMARY KEY,
        filename TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        id TEXT PRIMARY KEY,
        file_id TEXT,
        chunk_index INTEGER,
        chunk_text TEXT,
        FOREIGN KEY(file_id) REFERENCES files(id)
    );
    """)
    conn.commit()

def get_db_connection():
    return conn
