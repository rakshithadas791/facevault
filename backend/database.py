"""
Phase 1/3: Database layer
Tables:
  persons     -> id, name, created_at
  embeddings  -> id, person_id, embedding (stored as JSON string), created_at
  history     -> id, result_name, similarity, is_known, created_at
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "facevault.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            embedding TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (person_id) REFERENCES persons (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result_name TEXT NOT NULL,
            similarity REAL NOT NULL,
            is_known INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_person(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO persons (name, created_at) VALUES (?, ?)",
        (name, datetime.now().isoformat())
    )
    person_id = cur.lastrowid
    conn.commit()
    conn.close()
    return person_id


def add_embedding(person_id, embedding):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO embeddings (person_id, embedding, created_at) VALUES (?, ?, ?)",
        (person_id, json.dumps(embedding), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_embeddings():
    """Returns list of (person_id, name, embedding_list)"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT embeddings.person_id, persons.name, embeddings.embedding
        FROM embeddings
        JOIN persons ON embeddings.person_id = persons.id
    """)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "person_id": row["person_id"],
            "name": row["name"],
            "embedding": json.loads(row["embedding"])
        })
    return result


def get_all_persons():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM persons ORDER BY created_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def add_history(result_name, similarity, is_known):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (result_name, similarity, is_known, created_at) VALUES (?, ?, ?, ?)",
        (result_name, similarity, int(is_known), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_history(limit=50):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM history ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM persons")
    registered_users = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM history")
    total_recognitions = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM history WHERE is_known = 1")
    known = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM history WHERE is_known = 0")
    unknown = cur.fetchone()["c"]

    conn.close()

    return {
        "registered_users": registered_users,
        "total_recognitions": total_recognitions,
        "known": known,
        "unknown": unknown
    }
