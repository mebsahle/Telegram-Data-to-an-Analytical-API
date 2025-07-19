#!/usr/bin/env python3
"""
Wait for PostgreSQL database to be ready before running the application.
"""

import time
import sys
import psycopg2
from utils.config import PG_CONFIG

def wait_for_db(max_retries=30, delay=1):
    """Wait for database to become available."""
    print(f"Waiting for database at {PG_CONFIG['host']}:{PG_CONFIG['port']}...")
    
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            conn = psycopg2.connect(
                host=PG_CONFIG['host'],
                port=PG_CONFIG['port'],
                user=PG_CONFIG['user'],
                password=PG_CONFIG['password'],
                database=PG_CONFIG['database']
            )
            conn.close()
            print("Database is ready!")
            return True
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet... ({e})")
            time.sleep(delay)
    
    print("Database failed to become ready in time!")
    return False

if __name__ == "__main__":
    if wait_for_db():
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure
