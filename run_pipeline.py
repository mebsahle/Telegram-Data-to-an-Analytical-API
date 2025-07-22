#!/usr/bin/env python3
"""
Complete Telegram Medical Data Pipeline Runner
Runs scraping, image extraction, and YOLO inference in sequence.
"""

import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🚀 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Run the complete pipeline."""
    print("=" * 60)
    print("🏥 TELEGRAM MEDICAL DATA PIPELINE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    steps = [
        ("python ingestion/scraper.py", "Scraping Telegram messages and downloading images"),
        ("python ingestion/extract_images.py", "Organizing extracted images"),
        ("python enrichment/yolo_inference.py", "Running YOLO object detection"),
        ("python loading/loader.py", "Loading data to PostgreSQL database")
    ]
    
    successful_steps = 0
    
    for command, description in steps:
        if run_command(command, description):
            successful_steps += 1
        else:
            print(f"\n❌ Pipeline stopped due to failure in: {description}")
            break
    
    print("\n" + "=" * 60)
    print("📊 PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Completed steps: {successful_steps}/{len(steps)}")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if successful_steps == len(steps):
        print("🎉 Pipeline completed successfully!")
        
        # Show some stats
        try:
            import json
            detections_file = "data/enriched/detections.json"
            if os.path.exists(detections_file):
                with open(detections_file, 'r') as f:
                    detections = json.load(f)
                print(f"📷 Images processed: {len(detections)}")
                
                total_objects = sum(len(item.get("detected_objects", [])) for item in detections)
                print(f"🔍 Objects detected: {total_objects}")
        except Exception as e:
            print(f"Note: Could not load detection stats: {e}")
    else:
        print("⚠️  Pipeline completed with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
