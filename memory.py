import sqlite3
import re
from config import MEMORY_DATABASE

DATABASE = MEMORY_DATABASE


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_memory(key, value):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO memories (key, value)
        VALUES (?, ?)
    """, (key, value))

    connection.commit()
    connection.close()


def get_memory(key):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT value FROM memories WHERE key = ?",
        (key,)
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def get_all_memories():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT key, value FROM memories"
    )

    results = cursor.fetchall()

    connection.close()

    return results

def search_memories(query):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("SELECT key, value FROM memories")
    memories = cursor.fetchall()

    connection.close()

    query_words = re.findall(r"\b\w+\b", query.lower())

    relevant_memories = []

    for key, value in memories:
        key_words = re.findall(r"\b\w+\b", key.lower())
        value_words = re.findall(r"\b\w+\b", value.lower())

        memory_words = key_words + value_words

        for word in query_words:
            if word in memory_words:
                relevant_memories.append((key, value))
                break

    return relevant_memories