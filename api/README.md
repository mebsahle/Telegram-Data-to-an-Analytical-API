# Telegram Medical Data Analytics API

A comprehensive FastAPI-based REST API for analyzing medical data from Telegram channels.

## 🚀 Quick Start

### Using Docker (Recommended)
```bash
# Start all services including the API
docker-compose up -d

# The API will be available at:
# - API: http://localhost:8000
# - Documentation: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python start_api.py
# OR
cd api && uvicorn main:app --reload
```

## 📚 API Endpoints

### Core Analytics Endpoints

#### 1. Top Products Analysis
```http
GET /api/reports/top-products?limit=10&days=30
```
**Description**: Get most mentioned medical products/keywords
**Parameters**:
- `limit` (int): Number of top products (1-100, default: 10)
- `channel` (str, optional): Filter by specific channel
- `days` (int): Analysis period in days (1-365, default: 30)
- `min_mentions` (int): Minimum mentions required (default: 3)

**Example Response**:
```json
{
  "success": true,
  "message": "Retrieved top 5 products",
  "data": [
    {
      "keyword": "paracetamol",
      "mention_count": 25,
      "channels": ["CheMed123", "tikvahpharma"],
      "avg_views": 150.5,
      "trend_direction": "up",
      "sample_messages": ["Paracetamol 500mg available..."]
    }
  ]
}
```

#### 2. Channel Activity Analysis
```http
GET /api/channels/{channel_name}/activity?days=30
```
**Description**: Detailed activity analysis for a specific channel
**Parameters**:
- `channel_name` (str): Channel name (e.g., "CheMed123")
- `days` (int): Analysis period (1-365, default: 30)
- `include_keywords` (bool): Include keyword analysis (default: true)
- `keyword_limit` (int): Number of top keywords (1-50, default: 10)

**Example Response**:
```json
{
  "success": true,
  "data": {
    "channel": "CheMed123",
    "total_messages": 450,
    "avg_views": 125.5,
    "media_percentage": 35.2,
    "engagement_distribution": {
      "High": 50,
      "Medium": 200,
      "Low": 200
    },
    "recent_activity": [
      {
        "date": "2025-07-22",
        "message_count": 15,
        "total_views": 2500
      }
    ],
    "top_keywords": [
      {"keyword": "medicine", "frequency": 45},
      {"keyword": "delivery", "frequency": 32}
    ]
  }
}
```

#### 3. Message Search
```http
GET /api/search/messages?query=paracetamol&page=1&page_size=20
```
**Description**: Search messages across all channels
**Parameters**:
- `query` (str): Search term (required)
- `channel` (str, optional): Filter by channel
- `start_date` (datetime, optional): Start date filter
- `end_date` (datetime, optional): End date filter
- `has_media` (bool, optional): Filter by media presence
- `min_views` (int, optional): Minimum views filter
- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (1-100, default: 20)

### Utility Endpoints

#### 4. List Channels
```http
GET /api/channels
```
Get all available channels with basic stats.

#### 5. Object Detection Summary
```http
GET /api/detections/summary
```
Get summary of YOLO object detection results.

#### 6. Channel Detections
```http
GET /api/channels/{channel_name}/detections?limit=50
```
Get object detection results for a specific channel.

#### 7. Dashboard Data
```http
GET /api/analytics/dashboard?days=7
```
Get comprehensive dashboard data for visualization.

#### 8. Health Check
```http
GET /health
```
API health status check.

## 🏗️ Architecture

### Database Schema
The API connects to dbt-generated tables:
- **Raw Layer**: `raw.telegram_messages`
- **Staging Layer**: `dbt_public.stg_telegram_messages`
- **Marts Layer**: 
  - `dbt_public.dim_channels`
  - `dbt_public.dim_dates`
  - `dbt_public.fct_messages`
- **Enriched Layer**: `enriched.yolo_detections`

### Technology Stack
- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Validation**: Pydantic v2
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Deployment**: Docker with health checks

## 🔧 Configuration

### Environment Variables
```env
# Database Configuration
PGHOST=db
PGPORT=5432
PGUSER=mebsahle
PGPASSWORD=psql
PGDATABASE=kara_solutions
```

### CORS Configuration
Currently configured for development (`allow_origins=["*"]`). 
Update for production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 📊 Usage Examples

### Python Client Example
```python
import requests

# Get top products
response = requests.get(
    "http://localhost:8000/api/reports/top-products",
    params={"limit": 5, "days": 30}
)
products = response.json()["data"]

# Search for specific medication
response = requests.get(
    "http://localhost:8000/api/search/messages",
    params={"query": "paracetamol", "page_size": 10}
)
messages = response.json()["data"]["messages"]

# Get channel activity
response = requests.get(
    "http://localhost:8000/api/channels/CheMed123/activity",
    params={"days": 7}
)
activity = response.json()["data"]
```

### cURL Examples
```bash
# Top products
curl "http://localhost:8000/api/reports/top-products?limit=5"

# Channel activity
curl "http://localhost:8000/api/channels/CheMed123/activity?days=30"

# Search messages
curl "http://localhost:8000/api/search/messages?query=medicine&page=1"
```

## 🚨 Error Handling

The API uses standardized error responses:
```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_TYPE",
  "details": {...}
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid parameters)
- `404`: Not Found (channel/resource not found)
- `500`: Internal Server Error

## 🔒 Security Considerations

- Input validation with Pydantic
- SQL injection protection via SQLAlchemy ORM
- Rate limiting (implement as needed)
- Authentication/Authorization (implement as needed)
- HTTPS in production
- Environment variable protection

## 📈 Performance

- Database connection pooling
- Efficient pagination
- Query optimization
- Background task support (if needed)
- Caching layer (Redis - optional)

## 🧪 Testing

```bash
# Run API tests (when implemented)
pytest tests/api/

# Test API endpoints
curl http://localhost:8000/health
```

## 📝 Development

### Adding New Endpoints
1. Define Pydantic schemas in `schemas.py`
2. Create database operations in `crud.py`
3. Add endpoints in `main.py`
4. Update documentation

### Database Migrations
When dbt models change, update SQLAlchemy models in `models.py`.

## 🔗 Integration

This API integrates with:
- **dbt models** for clean, analytical data
- **YOLO detection results** for image analysis
- **PostgreSQL database** for storage
- **Docker environment** for deployment
- **Frontend applications** for visualization
