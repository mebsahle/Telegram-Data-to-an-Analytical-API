from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from api.database import Base

class TelegramMessage(Base):
    """Raw telegram messages table."""
    __tablename__ = "telegram_messages"
    __table_args__ = {"schema": "raw"}
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    text = Column(Text)
    views = Column(Integer)
    has_media = Column(Boolean)
    channel = Column(String(255))
    media_path = Column(String(500))

class StagingTelegramMessage(Base):
    """Staging telegram messages from dbt."""
    __tablename__ = "stg_telegram_messages"
    __table_args__ = {"schema": "dbt_public"}
    
    id = Column(Integer, primary_key=True)
    message_date = Column(DateTime)
    message_text = Column(Text)
    views = Column(Integer)
    has_media = Column(Boolean)
    channel = Column(String(255))
    loaded_at = Column(DateTime)

class DimChannel(Base):
    """Channel dimension table from dbt."""
    __tablename__ = "dim_channels"
    __table_args__ = {"schema": "dbt_public"}
    
    channel = Column(String(255), primary_key=True)
    total_messages = Column(Integer)
    first_message_date = Column(DateTime)
    last_message_date = Column(DateTime)

class DimDate(Base):
    """Date dimension table from dbt."""
    __tablename__ = "dim_dates"
    __table_args__ = {"schema": "dbt_public"}
    
    message_date = Column(DateTime, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    day_of_week = Column(Integer)

class FactMessage(Base):
    """Message facts table from dbt."""
    __tablename__ = "fct_messages"
    __table_args__ = {"schema": "dbt_public"}
    
    message_id = Column(Integer, primary_key=True)
    message_date = Column(DateTime)
    channel = Column(String(255))
    message_length = Column(Integer)
    views = Column(Integer)
    has_media = Column(Boolean)
    engagement_level = Column(String(50))
    loaded_at = Column(DateTime)

class YoloDetection(Base):
    """YOLO object detection results."""
    __tablename__ = "yolo_detections"
    __table_args__ = {"schema": "enriched"}
    
    id = Column(Integer, primary_key=True)
    file_path = Column(String(500))
    relative_path = Column(String(500))
    filename = Column(String(255))
    detected_objects = Column(Text)  # JSON array as text
    object_count = Column(Integer)
    confidence_score = Column(Float)
    created_at = Column(DateTime)
