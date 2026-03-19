import sqlite3

DB_NAME = "marks.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_marks_tables():  # real used for single-precision floating-point number
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS map_markers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                latitude REAL,
                longitude REAL
            )
        """)

    conn.commit()
    conn.close()

def reset_markers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM map_markers")  # remove all rows
    conn.commit()
    conn.close()

def add_marker(marker_type: str, latitude: float, longitude: float) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO map_markers (type, latitude, longitude)
        VALUES (?, ?, ?)
    """, (marker_type, latitude, longitude))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id  # return the auto-generated ID




def remove_marker(marker_id: int) -> bool:
    """Remove a marker by ID. Returns True if a row was deleted, False if not found."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM map_markers WHERE id = ?", (marker_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


def get_markers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, type, latitude, longitude FROM map_markers")
    markers = cursor.fetchall()

    conn.close()
    return markers