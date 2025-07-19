# Telegram Medical Data Pipeline

A comprehensive end-to-end data pipeline that scrapes messages from public Telegram channels focusing on medical/pharmaceutical content, processes and transforms the data using dbt, enriches it with YOLO object detection for medical images, and serves analytical insights through a FastAPI-based REST API.

## 🏗️ Architecture Overview

This pipeline implements a modern data engineering stack:

- **Data Ingestion**: Telethon-based Telegram scraper
- **Data Processing**: dbt for transformations and data modeling
- **ML Enhancement**: YOLO object detection for medical images
- **Data Storage**: PostgreSQL database
- **API Layer**: FastAPI for serving analytical endpoints
- **Orchestration**: Dagster for pipeline management
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
telegram_pipeline_project/
├── ingestion/                  # Telegram data scraping
│   ├── scraper.py             # Main scraper implementation
│   ├── logger.py              # Logging configuration
│   └── __init__.py
├── utils/                      # Shared utilities
│   ├── config.py              # Configuration management
│   ├── helpers.py             # Helper functions
│   └── __init__.py
├── data/                       # Data storage
│   └── raw/                   # Raw scraped data
│       └── telegram_messages/ # Daily organized messages
├── .env                       # Environment variables
├── .gitignore                # Git ignore rules
├── Dockerfile                # Container definition
├── docker-compose.yml        # Multi-service orchestration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Telegram API credentials

### 1. Environment Setup

Create your `.env` file with the following variables:

```env
# Telegram API Credentials
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone_number

# Database Configuration
POSTGRES_DB=telegram_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Other configurations
LOG_LEVEL=INFO
```

### 2. Run with Docker

Start all services using Docker Compose:

```bash
# Build and start services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Manual Setup (Alternative)

If you prefer to run without Docker:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the scraper
python ingestion/scraper.py
```

### 4. Access the Application

- **FastAPI Documentation**: http://localhost:8000/docs
- **Dagster UI**: http://localhost:3000
- **PostgreSQL**: localhost:5432

## 🎯 Target Channels

The pipeline currently scrapes from these medical/pharmaceutical Telegram channels:

- `lobelia4cosmetics` - Cosmetics and beauty products
- `tikvahpharma` - Pharmaceutical products
- `CheMed123` - Medical supplies and equipment

## 🔧 Key Features

### Data Ingestion
- **Automated Scraping**: Daily collection of messages, media, and metadata
- **Rate Limiting**: Respectful API usage with built-in delays
- **Error Handling**: Robust error recovery and logging
- **Session Management**: Persistent Telegram sessions

### Data Processing
- **Structured Storage**: JSON format with timestamp organization
- **Image Detection**: YOLO-based object detection for medical images
- **Data Transformation**: dbt models for clean, analytical datasets
- **Quality Assurance**: Data validation and cleaning pipelines

### API & Analytics
- **RESTful API**: FastAPI endpoints for data access
- **Real-time Insights**: Latest trends and patterns
- **Search Capabilities**: Full-text search across messages
- **Analytics Dashboard**: Key metrics and visualizations

## 📊 Data Schema

### Raw Message Structure
```json
{
  "id": "message_id",
  "date": "2025-07-19T10:30:00Z",
  "text": "message_content",
  "media": {
    "type": "photo|video|document",
    "file_path": "path/to/media",
    "detected_objects": ["medicine_bottle", "pill", "syringe"]
  },
  "channel": "channel_name",
  "views": 150,
  "forwards": 5
}
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Scraping** | Telethon | Telegram API client |
| **Database** | PostgreSQL | Data storage |
| **Transformation** | dbt | Data modeling |
| **ML/AI** | YOLO (Ultralytics) | Object detection |
| **API** | FastAPI | REST API server |
| **Orchestration** | Dagster | Pipeline management |
| **Containerization** | Docker | Environment isolation |
| **Validation** | Pydantic | Data validation |

## 🔍 API Endpoints

Once the FastAPI server is running, you can access:

- `GET /messages/` - Retrieve messages with filters
- `GET /channels/` - List monitored channels
- `GET /analytics/trends` - Get trending topics
- `GET /search/` - Search messages by content
- `GET /health/` - Service health check

## 📈 Monitoring & Logging

- **Structured Logging**: JSON-formatted logs with timestamps
- **Error Tracking**: Comprehensive error reporting
- **Performance Metrics**: Response times and throughput
- **Data Quality**: Validation and data freshness checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Mebatsion Sahle**
- GitHub: [@mebsahle](https://github.com/mebsahle)

## 🙏 Acknowledgments

- Telegram for providing the robust API
- Open source contributors of all the amazing libraries used
- Medical and pharmaceutical communities for public health information sharing
