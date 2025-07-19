import os, sys, json
from glob import glob
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from loading.models import telegram_messages, metadata
from utils.config import PG_CONFIG

# load .env
load_dotenv()

# Build database URL using config
DB_URL = (
    f"postgresql+psycopg2://{PG_CONFIG['user']}:"
    f"{PG_CONFIG['password']}@{PG_CONFIG['host']}:"
    f"{PG_CONFIG['port']}/{PG_CONFIG['database']}"
)

print(f"Connecting to database: {PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}")
print(f"Database URL: postgresql+psycopg2://{PG_CONFIG['user']}:***@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}")

# set up engine & session
try:
    engine = create_engine(DB_URL)
    # Test the connection
    with engine.connect() as conn:
        print("Database connection successful!")
        
        # Create schema if it doesn't exist
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
        conn.commit()
        print("Schema 'raw' created/verified")
        
    # Create all tables defined in metadata
    metadata.create_all(engine)
    print("Tables created/verified")
    
    Session = sessionmaker(bind=engine)
    session = Session()
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Make sure PostgreSQL is running and accessible")
    exit(1)

def load_file(filepath):
    channel = os.path.basename(filepath).replace('.json','')
    with open(filepath, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # Insert each record
    for msg in records:
        ins = telegram_messages.insert().values(
            id        = msg['id'],
            date      = msg['date'],
            text      = msg['text'],
            views     = msg.get('views'),
            has_media = msg.get('has_media', False),
            channel   = channel
        )
        try:
            session.execute(ins)
        except IntegrityError:
            session.rollback()      # skip duplicates
        else:
            session.commit()

def run_loader():
    for date_folder in os.listdir('data/raw/telegram_messages'):
        path = os.path.join('data/raw/telegram_messages', date_folder, '*.json')
        for filepath in glob(path):
            print(f"Loading {filepath}")
            load_file(filepath)

if __name__ == "__main__":
    run_loader()
    session.close()
