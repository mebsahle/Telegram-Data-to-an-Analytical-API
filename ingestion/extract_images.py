import os
import json
import shutil

RAW_DIR = "data/raw/telegram_messages"
IMAGE_OUTPUT_DIR = "data/raw/images"
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

def extract_images_from_json():
    """Extract and organize images from scraped telegram messages."""
    images_found = 0
    
    for root, _, files in os.walk(RAW_DIR):
        for file in files:
            if file.endswith(".json"):
                json_path = os.path.join(root, file)
                print(f"Processing: {json_path}")
                
                with open(json_path, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    
                for msg in messages:
                    # Check if message has media and media_path
                    if msg.get("has_media") and msg.get("media_path"):
                        source_path = msg["media_path"]
                        
                        # Check if the image file actually exists
                        if os.path.exists(source_path):
                            # Create organized directory structure
                            channel = msg.get("channel", "unknown")
                            organized_dir = os.path.join(IMAGE_OUTPUT_DIR, channel)
                            os.makedirs(organized_dir, exist_ok=True)
                            
                            filename = f"{channel}_{msg['id']}.jpg"
                            dest_path = os.path.join(organized_dir, filename)
                            
                            # Copy image to organized location if not already there
                            if source_path != dest_path:
                                shutil.copy2(source_path, dest_path)
                                print(f"Organized image: {filename}")
                            
                            images_found += 1
                        else:
                            print(f"Image file not found: {source_path}")
    
    print(f"✅ Image extraction complete. {images_found} images organized.")
    return images_found

if __name__ == "__main__":
    extract_images_from_json()