from ultralytics import YOLO
import os
import json
import cv2

MODEL_PATH = "yolov8n.pt"  # replace with medical-specific model if available
IMAGE_DIR = "data/raw/images"  # Look in images directory instead of messages
OUTPUT_PATH = "data/enriched/detections.json"

model = YOLO(MODEL_PATH)

def detect_objects(image_path):
    """Run YOLO inference on a single image and return detected objects."""
    try:
        results = model(image_path)
        objects = results[0].names
        detected = set()
        
        for r in results:
            if r.boxes is not None:
                for c in r.boxes.cls:
                    detected.add(objects[int(c)])
        
        return list(detected)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return []

def run_inference():
    """Run YOLO inference on all images in the image directory."""
    enriched_data = []
    processed_count = 0
    
    # Check if image directory exists
    if not os.path.exists(IMAGE_DIR):
        print(f"❌ Image directory {IMAGE_DIR} does not exist. Run image extraction first.")
        return
    
    # Process all images in subdirectories
    for root, _, files in os.walk(IMAGE_DIR):
        for f in files:
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):
                image_path = os.path.join(root, f)
                print(f"Processing: {image_path}")
                
                detected_objects = detect_objects(image_path)
                
                # Extract metadata from filename/path
                relative_path = os.path.relpath(image_path, IMAGE_DIR)
                
                enriched_data.append({
                    "file_path": image_path,
                    "relative_path": relative_path,
                    "filename": f,
                    "detected_objects": detected_objects,
                    "object_count": len(detected_objects)
                })
                
                processed_count += 1
                print(f"  → Detected: {detected_objects}")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Save results
    with open(OUTPUT_PATH, "w") as f:
        json.dump(enriched_data, f, indent=2)

    print(f"✅ YOLO inference complete. {processed_count} files processed.")
    
    # Print summary
    if enriched_data:
        total_objects = sum(len(item["detected_objects"]) for item in enriched_data)
        print(f"📊 Summary: {total_objects} total objects detected across {processed_count} images")
        
        # Show most common objects
        all_objects = []
        for item in enriched_data:
            all_objects.extend(item["detected_objects"])
        
        if all_objects:
            from collections import Counter
            common_objects = Counter(all_objects).most_common(5)
            print("🏆 Most common objects:")
            for obj, count in common_objects:
                print(f"   - {obj}: {count} times")

if __name__ == "__main__":
    run_inference()
