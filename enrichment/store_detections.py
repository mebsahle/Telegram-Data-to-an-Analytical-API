import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.config import get_db_connection
import json
from sqlalchemy import text

INPUT_PATH = "data/enriched/detections.json"

def store_detections():
    with open(INPUT_PATH, "r") as f:
        detections = json.load(f)

    conn = get_db_connection()

    with conn.begin():
        for record in detections:
            conn.execute(
                text("""
                    INSERT INTO yolo_detections (file_path, detected_objects)
                    VALUES (:file_path, :detected_objects)
                """),
                {
                    "file_path": record["file_path"],
                    "detected_objects": json.dumps(record["detected_objects"]),
                }
            )

    print(f"✅ {len(detections)} detections stored successfully.")

if __name__ == "__main__":
    store_detections()
