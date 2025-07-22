from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from api.database import get_db
from api.crud import MessageCRUD, DetectionCRUD
from api.schemas import (
    APIResponse, ErrorResponse, MessageResponse, ChannelResponse,
    TopProduct, ChannelActivity, SearchResult, DetectionResponse,
    MessageSearchParams, TopProductsParams, ChannelActivityParams
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Telegram Medical Data Analytics API",
    description="API for analyzing medical data from Telegram channels",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint."""
    return APIResponse(
        success=True,
        message="API is healthy",
        data={"status": "ok", "timestamp": datetime.now()}
    )

# Top products endpoint
@app.get("/api/reports/top-products", response_model=APIResponse)
async def get_top_products(
    limit: int = Query(10, ge=1, le=100, description="Number of top products"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    min_mentions: int = Query(3, ge=1, description="Minimum mentions required"),
    db: Session = Depends(get_db)
):
    """
    Get top mentioned medical products/keywords from Telegram channels.
    
    This endpoint analyzes message content to identify the most frequently
    mentioned medical products, medications, and healthcare-related terms.
    """
    try:
        params = TopProductsParams(
            limit=limit,
            channel=channel,
            days=days,
            min_mentions=min_mentions
        )
        
        top_products = MessageCRUD.get_top_products(db, params)
        
        return APIResponse(
            success=True,
            message=f"Retrieved top {len(top_products)} products",
            data=top_products,
            total_count=len(top_products)
        )
    
    except Exception as e:
        logger.error(f"Error getting top products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Channel activity endpoint
@app.get("/api/channels/{channel_name}/activity", response_model=APIResponse)
async def get_channel_activity(
    channel_name: str,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    include_keywords: bool = Query(True, description="Include keyword analysis"),
    keyword_limit: int = Query(10, ge=1, le=50, description="Number of top keywords"),
    db: Session = Depends(get_db)
):
    """
    Get detailed activity analysis for a specific Telegram channel.
    
    Provides comprehensive insights including message volume, engagement metrics,
    media usage, and trending keywords for the specified channel.
    """
    try:
        params = ChannelActivityParams(
            days=days,
            include_keywords=include_keywords,
            keyword_limit=keyword_limit
        )
        
        activity = MessageCRUD.get_channel_activity(db, channel_name, params)
        
        return APIResponse(
            success=True,
            message=f"Retrieved activity for channel {channel_name}",
            data=activity
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting channel activity: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Message search endpoint
@app.get("/api/search/messages", response_model=APIResponse)
async def search_messages(
    query: str = Query(..., min_length=1, description="Search query"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter"),
    has_media: Optional[bool] = Query(None, description="Filter by media presence"),
    min_views: Optional[int] = Query(None, ge=0, description="Minimum views filter"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Search messages across all Telegram channels.
    
    Supports full-text search with various filters including channel,
    date range, media presence, and view count thresholds.
    """
    try:
        params = MessageSearchParams(
            query=query,
            channel=channel,
            start_date=start_date,
            end_date=end_date,
            has_media=has_media,
            min_views=min_views,
            page=page,
            page_size=page_size
        )
        
        results = MessageCRUD.search_messages(db, params)
        
        return APIResponse(
            success=True,
            message=f"Found {results.total_count} messages matching query",
            data=results
        )
    
    except Exception as e:
        logger.error(f"Error searching messages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional utility endpoints

@app.get("/api/channels", response_model=APIResponse)
async def list_channels(db: Session = Depends(get_db)):
    """Get list of all available channels."""
    try:
        from api.models import DimChannel
        channels = db.query(DimChannel).all()
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(channels)} channels",
            data=channels,
            total_count=len(channels)
        )
    
    except Exception as e:
        logger.error(f"Error listing channels: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/detections/summary", response_model=APIResponse)
async def get_detection_summary(db: Session = Depends(get_db)):
    """Get summary of YOLO object detection results."""
    try:
        summary = DetectionCRUD.get_detection_summary(db)
        
        return APIResponse(
            success=True,
            message="Retrieved detection summary",
            data=summary
        )
    
    except Exception as e:
        logger.error(f"Error getting detection summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/detections", response_model=APIResponse)
async def get_channel_detections(
    channel_name: str,
    limit: int = Query(50, ge=1, le=200, description="Number of detections to return"),
    db: Session = Depends(get_db)
):
    """Get object detection results for a specific channel."""
    try:
        detections = DetectionCRUD.get_detections_by_channel(db, channel_name, limit)
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(detections)} detections for {channel_name}",
            data=detections,
            total_count=len(detections)
        )
    
    except Exception as e:
        logger.error(f"Error getting channel detections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/dashboard", response_model=APIResponse)
async def get_dashboard_data(
    days: int = Query(7, ge=1, le=90, description="Number of days for dashboard data"),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data."""
    try:
        from api.models import FactMessage, DimChannel
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Get basic stats
        total_messages = db.query(FactMessage).filter(
            FactMessage.message_date >= cutoff_date
        ).count()
        
        total_channels = db.query(DimChannel).count()
        
        # Get engagement distribution
        engagement_query = db.query(
            FactMessage.engagement_level,
            func.count(FactMessage.message_id).label('count')
        ).filter(
            FactMessage.message_date >= cutoff_date
        ).group_by(FactMessage.engagement_level).all()
        
        engagement_dist = {level: count for level, count in engagement_query}
        
        # Get top channels by activity
        channel_activity = db.query(
            FactMessage.channel,
            func.count(FactMessage.message_id).label('message_count'),
            func.avg(FactMessage.views).label('avg_views')
        ).filter(
            FactMessage.message_date >= cutoff_date
        ).group_by(FactMessage.channel)\
         .order_by(func.count(FactMessage.message_id).desc())\
         .limit(5).all()
        
        dashboard_data = {
            "period_days": days,
            "total_messages": total_messages,
            "total_channels": total_channels,
            "engagement_distribution": engagement_dist,
            "top_channels": [
                {
                    "channel": channel,
                    "message_count": msg_count,
                    "avg_views": float(avg_views) if avg_views else 0
                }
                for channel, msg_count, avg_views in channel_activity
            ]
        }
        
        return APIResponse(
            success=True,
            message="Retrieved dashboard data",
            data=dashboard_data
        )
    
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return ErrorResponse(
        success=False,
        message="Resource not found",
        error_code="NOT_FOUND"
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return ErrorResponse(
        success=False,
        message="Internal server error",
        error_code="INTERNAL_ERROR"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
