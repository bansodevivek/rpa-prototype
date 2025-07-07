# database/db_handler.py

import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Union

# Centralized DB path
DB_PATH = Path(r"C:\Users\ASUS\Prototype\rpa-prototype\output\quotes.db")

def ensure_output_dir():
    """Ensure the output directory exists."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_db_connection() -> sqlite3.Connection:
    """Create a database connection."""
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    """Initialize the database and create the quotes table."""
    ensure_output_dir()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                author TEXT NOT NULL,
                tags TEXT
            )
        ''')
        conn.commit()
    print(f"✅ Database initialized at {DB_PATH}")

def insert_quotes(quotes: List[Union[Dict[str, Optional[str]], tuple, list]]) -> None:
    """
    Insert quotes into the database.
    Accepts list of dicts with keys 'text', 'author', 'tags',
    or tuples/lists in the form (text, author, tags).
    """
    if not quotes:
        print("⚠️ No quotes to insert.")
        return

    normalized_quotes = []

    for q in quotes:
        if isinstance(q, dict):
            text = q.get('text')
            author = q.get('author')
            tags = q.get('tags', '') or ''
        elif isinstance(q, (list, tuple)):
            # Assuming tuple/list order: (text, author, tags)
            if len(q) >= 2:
                text = q[0]
                author = q[1]
                tags = q[2] if len(q) > 2 else ''
            else:
                print(f"⚠️ Skipping quote with insufficient data: {q}")
                continue
        else:
            print(f"⚠️ Skipping unknown quote format: {q}")
            continue

        if text and author:
            normalized_quotes.append({
                'text': str(text).strip(),
                'author': str(author).strip(),
                'tags': str(tags).strip()
            })
        else:
            print(f"⚠️ Skipping quote missing text or author: {q}")

    if not normalized_quotes:
        print("⚠️ No valid quotes to insert after normalization.")
        return

    ensure_output_dir()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO quotes (text, author, tags)
                VALUES (:text, :author, :tags)
            ''', normalized_quotes)
            conn.commit()
        print(f"✅ Inserted {len(normalized_quotes)} quotes into the database.")
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
