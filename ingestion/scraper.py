import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from ingestion.logger import scrape_logger
from utils.config import TELEGRAM_API_ID, TELEGRAM_API_HASH
from utils.helpers import ensure_dir


CHANNELS = [
    'https://t.me/lobelia4cosmetics',
    'https://t.me/tikvahpharma',
    'https://t.me/CheMed123'
]

BASE_DIR = "data/raw/telegram_messages"

def fetch_messages(channel_url, limit=200):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    channel_name = channel_url.split("/")[-1]
    output_dir = os.path.join(BASE_DIR, today)
    ensure_dir(output_dir)

    filename = os.path.join(output_dir, f"{channel_name}.json")
    scrape_logger.info(f"Fetching messages from {channel_name}...")

    try:
        with TelegramClient("scraper_session", TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            messages = []
            for msg in client.iter_messages(channel_url, limit=limit):
                messages.append({
                    "id": msg.id,
                    "date": str(msg.date),
                    "text": msg.message,
                    "views": msg.views,
                    "has_media": isinstance(msg.media, MessageMediaPhoto)
                })

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2, ensure_ascii=False)

            scrape_logger.info(f"Saved {len(messages)} messages from {channel_name} to {filename}")

    except Exception as e:
        scrape_logger.error(f"Failed to fetch {channel_name}: {str(e)}")

def run_all():
    for channel in CHANNELS:
        fetch_messages(channel)

if __name__ == "__main__":
    run_all()
