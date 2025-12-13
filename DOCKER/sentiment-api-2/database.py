import sqlite3
from typing import List, Tuple

DB_PATH = "predictions.db"


def get_connection():
    "return  a sqllite3 connection"
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    return conn

def create_table():
    "create predictions table if doesn't exists."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        confidence REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()


def save_predictions( text:str, sentiment: int, confidence: float ):
    "Insert a prediction row."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions( text, sentiment, confidence ) VALUES(?,?,?)",
        (text,str(sentiment), float(confidence) )
    )
    conn.commit()
    conn.close()

def get_history( limit: int =10 ) -> List[Tuple]:
    "return last `limit` predictions (most recent first)."
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id,text,sentiment,confidence, timestamp FROM predictions ORDER BY timestamp DESC LIMIT ?",
        (int(limit),)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

