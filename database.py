import sqlite3
from datetime import datetime

DATABASE_NAME = "audit_database.db"


# Connect to database
def connect_database():

    return sqlite3.connect(DATABASE_NAME)


# Create all database tables
def create_tables():

    connection = connect_database()
    cursor = connection.cursor()

    # Audit results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue TEXT,
        column_name TEXT,
        count INTEGER,
        audit_date TEXT
    )
    """)

    # Pipeline logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pipeline_name TEXT,
        status TEXT,
        records_processed INTEGER,
        execution_time REAL,
        start_time TEXT,
        error_message TEXT
    )
    """)

    # AI anomaly results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anomaly_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        amount REAL,
        prediction INTEGER,
        status TEXT,
        detected_at TEXT
    )
    """)

    connection.commit()
    connection.close()


# Save audit results
def save_audit_result(issue, column_name, count):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
    INSERT INTO audit_results
    (issue, column_name, count, audit_date)
    VALUES (?, ?, ?, ?)
    """,
        (issue, column_name, count, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )

    connection.commit()
    connection.close()


# Save pipeline information
def save_pipeline_log(name, status, records, execution_time, start_time, error):

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        """
    INSERT INTO pipeline_logs
    (
        pipeline_name,
        status,
        records_processed,
        execution_time,
        start_time,
        error_message
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (name, status, records, execution_time, start_time, error),
    )

    connection.commit()
    connection.close()


# Save AI anomaly results
def save_anomalies(results):

    connection = connect_database()
    cursor = connection.cursor()

    # Keep only the latest detection results
    cursor.execute("DELETE FROM anomaly_results")

    for index, row in results.iterrows():

        cursor.execute(
            """
        INSERT INTO anomaly_results
        (order_id, amount, prediction, status, detected_at)
        VALUES (?, ?, ?, ?, ?)
        """,
            (
                int(row["order_id"]),
                float(row["amount"]),
                int(row["prediction"]),
                row["status"],
                row["detected_at"],
            ),
        )

    connection.commit()
    connection.close()


# Read database table
def read_table(table_name):

    allowed_tables = ["audit_results", "pipeline_logs", "anomaly_results"]

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name")

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM " + table_name)

    results = cursor.fetchall()

    connection.close()

    return results


# Create database tables automatically
create_tables()
