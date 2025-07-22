import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import get_db_connection
from sqlalchemy import text

def create_yolo_detections_table():
    conn = get_db_connection()

    create_table_sql = text("""
        CREATE TABLE IF NOT EXISTS yolo_detections (
            id SERIAL PRIMARY KEY,
            file_path TEXT NOT NULL,
            detected_objects JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    with conn.begin():
        conn.execute(create_table_sql)

    print("✅ Table 'yolo_detections' created successfully.")

if __name__ == "__main__":
    create_yolo_detections_table()
