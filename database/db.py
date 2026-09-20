import sqlite3
DATABASE_FILE = "database/campusfix.db"
def get_connection():
    return sqlite3.connect(DATABASE_FILE)
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint TEXT NOT NULL,
            likely_cause TEXT,
            confidence TEXT,
            recommended_fix TEXT,
            estimated_cost TEXT,
            estimated_time TEXT,
            urgency TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER,
            feedback TEXT,
            actual_cause TEXT,
            actual_resolution TEXT,
            actual_cost TEXT,
            actual_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()
def save_complaint(
    complaint,
    likely_cause,
    confidence,
    recommended_fix,
    estimated_cost,
    estimated_time,
    urgency,
    explanation
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO complaints (
            complaint,
            likely_cause,
            confidence,
            recommended_fix,
            estimated_cost,
            estimated_time,
            urgency,
            explanation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        complaint,
        likely_cause,
        confidence,
        recommended_fix,
        estimated_cost,
        estimated_time,
        urgency,
        explanation
    ))

    connection.commit()
    connection.close()
def get_complaints():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM complaints
        ORDER BY created_at DESC
    """)

    complaints = cursor.fetchall()

    connection.close()

    return complaints
def save_feedback(
    complaint_id,
    feedback,
    actual_cause="",
    actual_resolution="",
    actual_cost="",
    actual_time=""
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO feedback (
            complaint_id,
            feedback,
            actual_cause,
            actual_resolution,
            actual_cost,
            actual_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        complaint_id,
        feedback,
        actual_cause,
        actual_resolution,
        actual_cost,
        actual_time
    ))

    connection.commit()
    connection.close()
def get_latest_complaint_id():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM complaints
        ORDER BY id DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None