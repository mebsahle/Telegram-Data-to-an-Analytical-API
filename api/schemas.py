from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Base schemas
class MessageBase(BaseModel):
    """Base message schema."""
    id: int
    message_date: datetime
    message_text: Optional[str] = None
    views: Optional[int] = 0
    has_media: bool = False
    channel: str

class MessageResponse(MessageBase):
    """Response schema for message data."""
    message_length: Optional[int] = 0
    engagement_level: Optional[str] = None
    loaded_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ChannelBase(BaseModel):
    """Base channel schema."""
    channel: str
    total_messages: int
    first_message_date: Optional[datetime] = None
    last_message_date: Optional[datetime] = None

class ChannelResponse(ChannelBase):
    """Response schema for channel data."""
    class Config:
        from_attributes = True

class ChannelActivity(BaseModel):
    """Channel activity analysis."""
    channel: str
    total_messages: int
    avg_views: float
    media_percentage: float
    engagement_distribution: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
    top_keywords: List[Dict[str, Any]]

class TopProduct(BaseModel):
    """Top product/keyword analysis."""
    keyword: str
    mention_count: int
    channels: List[str]
    avg_views: float
    trend_direction: str  # "up", "down", "stable"
    sample_messages: List[str]

class SearchResult(BaseModel):
    """Search result schema."""
    total_count: int
    page: int
    page_size: int
    messages: List[MessageResponse]

class DetectionBase(BaseModel):
    """Base detection schema."""
    file_path: str
    relative_path: str
    filename: str
    detected_objects: List[str]
    object_count: int

class DetectionResponse(DetectionBase):
    """Response schema for detection data."""
    id: int
    confidence_score: Optional[float] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# API Response wrappers
class APIResponse(BaseModel):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None
    total_count: Optional[int] = None

class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

# Query parameters
class MessageSearchParams(BaseModel):
    """Search parameters for messages."""
    query: str = Field(..., min_length=1, description="Search query")
    channel: Optional[str] = Field(None, description="Filter by channel")
    start_date: Optional[datetime] = Field(None, description="Start date filter")
    end_date: Optional[datetime] = Field(None, description="End date filter")
    has_media: Optional[bool] = Field(None, description="Filter by media presence")
    min_views: Optional[int] = Field(None, ge=0, description="Minimum views filter")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")

class TopProductsParams(BaseModel):
    """Parameters for top products endpoint."""
    limit: int = Field(10, ge=1, le=100, description="Number of top products")
    channel: Optional[str] = Field(None, description="Filter by channel")
    days: Optional[int] = Field(30, ge=1, le=365, description="Number of days to analyze")
    min_mentions: int = Field(3, ge=1, description="Minimum mentions required")

class ChannelActivityParams(BaseModel):
    """Parameters for channel activity analysis."""
    days: int = Field(30, ge=1, le=365, description="Number of days to analyze")
    include_keywords: bool = Field(True, description="Include keyword analysis")
    keyword_limit: int = Field(10, ge=1, le=50, description="Number of top keywords")
