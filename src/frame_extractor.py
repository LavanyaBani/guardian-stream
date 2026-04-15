from __future__ import annotations
import logging
import os
from pathlib import Path
from google.cloud import storage
import cv2

# ==========================================
# STEP 1: INITIALIZE CLIENT & PATHS (GLOBAL)
# ==========================================
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
key_path = project_root / "service-account-key.json"

if not key_path.exists():
    raise FileNotFoundError(f"CRITICAL: Key not found at {key_path}")

print(f"✅ Found Key File: {key_path}")

try:
    STORAGE_CLIENT = storage.Client.from_service_account_json(str(key_path))
    print(f"✅ Client Initialized! Project: {STORAGE_CLIENT.project}")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")
    raise e

# --- Define ALL Paths Here ---
ORIGINAL_DIR = project_root / "data" / "original" / "real_sports"
SAMPLE_EDITED_DIR = project_root / "data" / "sample_edited" / "edited_real"
DEEPFAKE_DIR = project_root / "data" / "sample_edited" / "deepfake_mismatch" # Added Deepfake

TEMP_ROOT = project_root / "temp_frames" # Fixed: Defined globally

ORIGINAL_BUCKET = "guardian-original-frames-lavanya"
SAMPLE_EDITED_BUCKET = "guardian-sample_edited-frames-lavanya"

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ==========================================
# STEP 2: HELPER FUNCTIONS
# ==========================================
def scan_mp4s() -> list[Path]:
    videos = []
    folders_to_scan = [ORIGINAL_DIR, SAMPLE_EDITED_DIR, DEEPFAKE_DIR]
    
    print(f"\n🔍 Scanning {len(folders_to_scan)} folders...")
    for folder in folders_to_scan:
        if not folder.exists():
            logger.warning(f"Folder missing: {folder}")
            continue
        count = len([f for f in folder.iterdir() if f.suffix.lower() == ".mp4"])
        print(f"   Found {count} videos in {folder.name}")
        for item in sorted(folder.iterdir()):
            if item.is_file() and item.suffix.lower() == ".mp4":
                videos.append(item)
    return videos

def detect_bucket(video_path: Path):
    path_str = str(video_path).lower()
    if "original" in path_str:
        return ORIGINAL_BUCKET, "ORIGINAL"
    if "sample_edited" in path_str or "deepfake" in path_str:
        return SAMPLE_EDITED_BUCKET, "DEEPFAKE_MISMATCH"
    raise ValueError(f"Unknown video type: {video_path}")

def extract_frames(video_path: Path, temp_dir: Path):
    temp_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0: fps = 25
    step = max(1, int(round(fps)))
    
    frames = []
    idx = 0
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if idx % step == 0:
            count += 1
            fname = temp_dir / f"frame_{count:03d}.jpg"
            try:
                cv2.imwrite(str(fname), frame)
                frames.append(fname)
            except Exception as e:
                logger.error(f"Failed to write frame {fname}: {e}")
        idx += 1
    cap.release()
    return frames

def upload_frames(client, bucket_name, video_name, frame_paths):
    bucket = client.bucket(bucket_name)
    for f_path in frame_paths:
        blob = bucket.blob(f"{video_name}/{f_path.name}")
        blob.upload_from_filename(str(f_path), content_type="image/jpeg")
    print(f"   >>> Uploaded {len(frame_paths)} frames to {bucket_name}")

# ==========================================
# STEP 3: MAIN FUNCTION
# ==========================================
def main(client):
    videos = scan_mp4s()
    if not videos:
        logger.error("No videos found!")
        return 1
    
    for video in videos:
        print(f"\n>>> Processing: {video.name}")
        try:
            b_name, v_type = detect_bucket(video)
            print(f"   >>> Type: {v_type}")
            
            # Sanitize video name for folder creation (remove special chars)
            safe_name = "".join([c if c.isalnum() or c in "._-" else "_" for c in video.stem])
            temp_dir = TEMP_ROOT / safe_name
            
            frames = extract_frames(video, temp_dir)
            
            if not frames:
                logger.warning("No frames extracted.")
                continue
                
            upload_frames(client, b_name, safe_name, frames)
        except Exception as e:
            logger.error(f"Failed {video.name}: {e}")
            
    print("\n✅ All done!")
    return 0

if __name__ == "__main__":
    main(STORAGE_CLIENT)
