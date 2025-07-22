import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables from .env
load_dotenv()

# Telegram API credentials
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

# PostgreSQL config
PG_CONFIG = {
    "host": os.getenv("PGHOST"),
    "port": int(os.getenv("PGPORT", 5432)),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "database": os.getenv("PGDATABASE"),
}

def get_db_connection():
    url = f"postgresql+psycopg2://{PG_CONFIG['user']}:{PG_CONFIG['password']}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"
    engine = create_engine(url)
    return engine.connect()
