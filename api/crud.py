import json
import re
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, text, desc, asc, and_, or_
from collections import Counter

from api.models import (
    TelegramMessage, StagingTelegramMessage, DimChannel, 
    FactMessage, YoloDetection
)
from api.schemas import (
    MessageSearchParams, TopProductsParams, ChannelActivityParams,
    TopProduct, ChannelActivity, SearchResult
)

class MessageCRUD:
    """CRUD operations for messages."""
    
    @staticmethod
    def search_messages(db: Session, params: MessageSearchParams) -> SearchResult:
        """Search messages with filters and pagination."""
        query = db.query(FactMessage)
        
        # Apply filters
        if params.query:
            # Search in message text (join with staging table for text)
            query = query.join(
                StagingTelegramMessage, 
                FactMessage.message_id == StagingTelegramMessage.id
            )
            query = query.filter(
                StagingTelegramMessage.message_text.ilike(f"%{params.query}%")
            )
        
        if params.channel:
            query = query.filter(FactMessage.channel == params.channel)
        
        if params.start_date:
            query = query.filter(FactMessage.message_date >= params.start_date)
        
        if params.end_date:
            query = query.filter(FactMessage.message_date <= params.end_date)
        
        if params.has_media is not None:
            query = query.filter(FactMessage.has_media == params.has_media)
        
        if params.min_views:
            query = query.filter(FactMessage.views >= params.min_views)
        
        # Get total count
        total_count = query.count()
        
        # Apply pagination
        offset = (params.page - 1) * params.page_size
        messages = query.order_by(desc(FactMessage.message_date))\
                       .offset(offset)\
                       .limit(params.page_size)\
                       .all()
        
        return SearchResult(
            total_count=total_count,
            page=params.page,
            page_size=params.page_size,
            messages=messages
        )
    
    @staticmethod
    def get_top_products(db: Session, params: TopProductsParams) -> List[TopProduct]:
        """Get top mentioned products/keywords."""
        # Define medical/pharmaceutical keywords to search for
        medical_keywords = [
            "paracetamol", "ibuprofen", "aspirin", "amoxicillin", "omeprazole",
            "metformin", "insulin", "vitamin", "antibiotic", "painkiller",
            "medicine", "tablet", "capsule", "syrup", "injection", "vaccine",
            "pharmacy", "prescription", "dosage", "treatment", "therapy"
        ]
        
        cutoff_date = datetime.now() - timedelta(days=params.days)
        
        # Get messages from the specified period
        query = db.query(StagingTelegramMessage)\
                 .filter(StagingTelegramMessage.message_date >= cutoff_date)
        
        if params.channel:
            query = query.filter(StagingTelegramMessage.channel == params.channel)
        
        messages = query.all()
        
        # Count keyword mentions
        keyword_stats = {}
        for message in messages:
            if not message.message_text:
                continue
                
            text_lower = message.message_text.lower()
            for keyword in medical_keywords:
                if keyword in text_lower:
                    if keyword not in keyword_stats:
                        keyword_stats[keyword] = {
                            'count': 0,
                            'channels': set(),
                            'total_views': 0,
                            'message_count': 0,
                            'sample_messages': []
                        }
                    
                    keyword_stats[keyword]['count'] += 1
                    keyword_stats[keyword]['channels'].add(message.channel)
                    keyword_stats[keyword]['total_views'] += message.views or 0
                    keyword_stats[keyword]['message_count'] += 1
                    
                    # Add sample message (first 100 chars)
                    if len(keyword_stats[keyword]['sample_messages']) < 3:
                        sample = message.message_text[:100] + "..." if len(message.message_text) > 100 else message.message_text
                        keyword_stats[keyword]['sample_messages'].append(sample)
        
        # Filter by minimum mentions and convert to TopProduct objects
        top_products = []
        for keyword, stats in keyword_stats.items():
            if stats['count'] >= params.min_mentions:
                avg_views = stats['total_views'] / stats['message_count'] if stats['message_count'] > 0 else 0
                
                top_products.append(TopProduct(
                    keyword=keyword,
                    mention_count=stats['count'],
                    channels=list(stats['channels']),
                    avg_views=avg_views,
                    trend_direction="stable",  # TODO: Implement trend analysis
                    sample_messages=stats['sample_messages']
                ))
        
        # Sort by mention count and return top N
        top_products.sort(key=lambda x: x.mention_count, reverse=True)
        return top_products[:params.limit]
    
    @staticmethod
    def get_channel_activity(db: Session, channel_name: str, params: ChannelActivityParams) -> ChannelActivity:
        """Get detailed channel activity analysis."""
        cutoff_date = datetime.now() - timedelta(days=params.days)
        
        # Get channel stats from dimension table
        channel_dim = db.query(DimChannel)\
                       .filter(DimChannel.channel == channel_name)\
                       .first()
        
        if not channel_dim:
            raise ValueError(f"Channel '{channel_name}' not found")
        
        # Get message facts for the period
        messages_query = db.query(FactMessage)\
                          .filter(FactMessage.channel == channel_name)\
                          .filter(FactMessage.message_date >= cutoff_date)
        
        messages = messages_query.all()
        
        # Calculate statistics
        total_messages = len(messages)
        avg_views = sum(msg.views or 0 for msg in messages) / total_messages if total_messages > 0 else 0
        media_count = sum(1 for msg in messages if msg.has_media)
        media_percentage = (media_count / total_messages * 100) if total_messages > 0 else 0
        
        # Engagement distribution
        engagement_dist = Counter(msg.engagement_level for msg in messages if msg.engagement_level)
        
        # Recent activity (last 7 days by day)
        recent_activity = []
        for i in range(7):
            day_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            day_messages = [msg for msg in messages if day_start <= msg.message_date < day_end]
            recent_activity.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "message_count": len(day_messages),
                "total_views": sum(msg.views or 0 for msg in day_messages)
            })
        
        # Top keywords (if requested)
        top_keywords = []
        if params.include_keywords:
            # Get message texts for keyword analysis
            text_messages = db.query(StagingTelegramMessage)\
                             .filter(StagingTelegramMessage.channel == channel_name)\
                             .filter(StagingTelegramMessage.message_date >= cutoff_date)\
                             .all()
            
            # Extract keywords (simple word frequency)
            word_freq = Counter()
            for msg in text_messages:
                if msg.message_text:
                    # Simple word extraction (remove common words)
                    words = re.findall(r'\b\w{4,}\b', msg.message_text.lower())
                    for word in words:
                        if word not in ['that', 'this', 'with', 'from', 'they', 'have', 'will', 'been', 'were']:
                            word_freq[word] += 1
            
            top_keywords = [
                {"keyword": word, "frequency": freq}
                for word, freq in word_freq.most_common(params.keyword_limit)
            ]
        
        return ChannelActivity(
            channel=channel_name,
            total_messages=total_messages,
            avg_views=avg_views,
            media_percentage=media_percentage,
            engagement_distribution=dict(engagement_dist),
            recent_activity=recent_activity,
            top_keywords=top_keywords
        )

class DetectionCRUD:
    """CRUD operations for YOLO detections."""
    
    @staticmethod
    def get_detections_by_channel(db: Session, channel: str, limit: int = 50) -> List[YoloDetection]:
        """Get object detections for a specific channel."""
        return db.query(YoloDetection)\
                .filter(YoloDetection.relative_path.like(f"%{channel}%"))\
                .order_by(desc(YoloDetection.created_at))\
                .limit(limit)\
                .all()
    
    @staticmethod
    def get_detection_summary(db: Session) -> Dict[str, Any]:
        """Get summary of all detections."""
        total_detections = db.query(YoloDetection).count()
        
        # Get most common objects
        detections = db.query(YoloDetection).all()
        all_objects = []
        for detection in detections:
            if detection.detected_objects:
                # Assuming detected_objects is stored as JSON string
                try:
                    objects = json.loads(detection.detected_objects)
                    all_objects.extend(objects)
                except:
                    # If it's already a list or simple string
                    if isinstance(detection.detected_objects, list):
                        all_objects.extend(detection.detected_objects)
        
        object_freq = Counter(all_objects)
        
        return {
            "total_detections": total_detections,
            "total_objects": len(all_objects),
            "unique_objects": len(object_freq),
            "most_common_objects": object_freq.most_common(10)
        }
