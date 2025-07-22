import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

# Import configuration
from utils.config import PG_CONFIG

# Build database URL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{PG_CONFIG['user']}:{PG_CONFIG['password']}@"
    f"{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"
)

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """Dependency function to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
