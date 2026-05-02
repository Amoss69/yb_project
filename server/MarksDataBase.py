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
                longitude REAL,
                room_id INTEGER
            )
        """)

    conn.commit()
    conn.close()

def reset_markers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM map_markers")  # wipes all markers across all rooms
    conn.commit()
    conn.close()

def add_marker(marker_type: str, latitude: float, longitude: float, room_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO map_markers (type, latitude, longitude, room_id)
        VALUES (?, ?, ?, ?)
    """, (marker_type, latitude, longitude, room_id))

    conn.commit()
    new_id = cursor.lastrowid # sqlite gives us the id it just assigned
    conn.close()
    return new_id  # return the auto-generated ID




def remove_marker(marker_id: int) -> bool:
    #Remove a marker by ID. Returns True if a row was deleted, False if not found.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM map_markers WHERE id = ?", (marker_id,))
    deleted = cursor.rowcount > 0 # rowcount 0 means no row matched that id

    conn.commit()
    conn.close()

    return deleted


def get_markers(room_id: int):  # filter by room
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, latitude, longitude FROM map_markers WHERE room_id = ?", (room_id,))
    markers = cursor.fetchall()
    conn.close()
    return markers # list of (id, type, lat, lng) tuples