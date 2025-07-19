# 🧬 Telegram Medical Data Pipeline

A full-stack, end-to-end data pipeline that scrapes medical-related messages from public Telegram channels, enriches them with YOLO-based image detection, models the data using dbt, and exposes insights through a RESTful API built with FastAPI.

---

## 🏗️ Architecture Overview

This pipeline implements a modern data engineering stack:

| Layer            | Technology      | Purpose                           |
|------------------|------------------|-----------------------------------|
| Ingestion        | Telethon         | Scrape Telegram messages          |
| Processing       | dbt              | SQL-based transformation          |
| ML Enrichment    | YOLOv8 (Ultralytics) | Medical image object detection |
| Storage          | PostgreSQL       | Relational data storage           |
| API Layer        | FastAPI          | REST endpoints for analytics      |
| Orchestration    | Dagster          | Pipeline scheduling & orchestration |
| Containerization | Docker + Compose | Service isolation and deployment |

---

## 📁 Project Structure

```

telegram\_pipeline\_project/
├── ingestion/
│   ├── scraper.py
│   ├── logger.py
│   └── **init**.py
├── utils/
│   ├── config.py
│   ├── helpers.py
│   └── **init**.py
├── data/
│   └── raw/
│       └── telegram\_messages/
├── telegram\_dbt/                # dbt project
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg\_telegram\_messages.sql
│   │   ├── marts/
│   │   │   ├── dim\_channels.sql
│   │   │   ├── dim\_dates.sql
│   │   │   └── fct\_messages.sql
│   │   └── schema.yml
│   ├── dbt\_project.yml
│   └── ...
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

````

---

## 🛠️ Setup Instructions

### ✅ Prerequisites

- Docker + Docker Compose
- Python 3.10+
- Telegram API credentials from https://my.telegram.org

---

### 🧪 1. Clone and Set Up the Project

```bash
git clone https://github.com/mebsahle/telegram_pipeline_project.git
cd telegram_pipeline_project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

---

### 🔐 2. Create `.env`

```env
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_PHONE=your_phone
POSTGRES_DB=kara_solutions
POSTGRES_USER=your_username
POSTGRES_PASSWORD=psql
POSTGRES_PORT=5432
POSTGRES_HOST=db
LOG_LEVEL=INFO
```

---

### 🐳 3. Start the Pipeline with Docker

```bash
docker-compose up --build -d
```

* FastAPI: [http://localhost:8000](http://localhost:8000)
* PostgreSQL: localhost:5432
* Dagster UI: [http://localhost:3000](http://localhost:3000)

---

### ⚙️ 4. Run the Scraper

```bash
docker exec -it telegram_pipeline_project-app-1 bash
python ingestion/scraper.py
```

---

### 🧠 5. Run dbt Models

```bash
docker exec -it telegram_pipeline_project-app-1 bash
cd telegram_dbt
dbt run      # Build models
dbt test     # Run tests
dbt docs generate && dbt docs serve  # Visual docs (http://localhost:8080)
```

---

## 🧪 dbt Tests (Task 2)

Tests are defined in `schema.yml` and include:

* `unique` + `not_null` on `id`, `channel_name`, `message_date`
* `dim_dates.date` and `dim_channels.channel_name` uniqueness checks

Run them with:

```bash
dbt test
```

---

## 📦 YOLO Image Enrichment (Task 3 Preview)

* Run YOLOv8 on downloaded Telegram media
* Store detections in `fct_image_detections`
* Model relationships via dbt joins to `fct_messages`

> YOLO integration begins in Task 3.

---

## 📊 Example Data Structure

```json
{
  "id": "msg12345",
  "date": "2025-07-19T12:34:00Z",
  "text": "New medical supplies in stock!",
  "media": {
    "type": "photo",
    "file_path": "/media/img_20250719.jpg",
    "detected_objects": ["pill", "syringe"]
  },
  "channel": "CheMed123",
  "views": 192,
  "forwards": 3
}
```

---

## 📡 API Endpoints (FastAPI)

| Method | Endpoint            | Description             |
| ------ | ------------------- | ----------------------- |
| GET    | `/messages/`        | Fetch all messages      |
| GET    | `/channels/`        | List all channels       |
| GET    | `/analytics/trends` | View trending terms     |
| GET    | `/search/?q=query`  | Search text in messages |
| GET    | `/health/`          | Health check            |

---

## 👨‍💻 Git Workflow

```bash
git checkout -b feature/dbt-models
# Make changes...
git add .
git commit -m "Add dbt models and schema tests"
git push -u origin feature/dbt-models
```

Then open a Pull Request and merge to `main` after review.

---

## 👤 Author

**Mebatsion Sahle**
GitHub: [@mebsahle](https://github.com/mebsahle)

---

## 📄 License

MIT License – see `LICENSE` file for details.

---

## 🙏 Acknowledgments

* [Telethon](https://github.com/LonamiWebs/Telethon)
* [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
* [dbt Labs](https://www.getdbt.com/)
* [Dagster](https://dagster.io/)

