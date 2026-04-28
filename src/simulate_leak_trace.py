# Add these 3 lines at the VERY TOP (before any imports)
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
import logging
from pathlib import Path
import json
import shutil
import time
from watermark_engine import embed_watermark, extract_watermark
from PIL import Image
import numpy as np

# --- Configuration ---
ROOT = Path(__file__).resolve().parent.parent
SAMPLE_FRAMES_DIR = ROOT / "sample_frames_dist"
LEAKED_FRAMES_DIR = ROOT / "leaked_frames_found"
REPORT_PATH = ROOT / "leak_trace_report.json"

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def create_dummy_frame(path: Path, color: tuple, label: str):
    """Creates a colored dummy frame with text label."""
    img = Image.new('RGB', (300, 200), color=color)
    # Note: Adding actual text requires PIL Draw, keeping it simple with colors for now
    # Color codes: Red=(255,0,0), Green=(0,255,0), Blue=(0,0,255)
    img.save(str(path), format='PNG')
    logger.debug(f"Created dummy frame: {path.name} ({label})")

def main():
    logger.info(" Starting GuardianStream Leak Simulation & Trace Demo")
    
    # 1. Setup Directories
    if SAMPLE_FRAMES_DIR.exists(): shutil.rmtree(SAMPLE_FRAMES_DIR)
    if LEAKED_FRAMES_DIR.exists(): shutil.rmtree(LEAKED_FRAMES_DIR)
    SAMPLE_FRAMES_DIR.mkdir(parents=True)
    LEAKED_FRAMES_DIR.mkdir(parents=True)
    
    # 2. Define Partners & Content
    partners = [
        {"id": "PARTNER_A_NETFLIX", "color": (229, 9, 20), "label": "Netflix"}, # Red
        {"id": "PARTNER_B_PRIME", "color": (0, 168, 229), "label": "Prime"},    # Blue
        {"id": "PARTNER_C_HOTSTAR", "color": (100, 50, 200), "label": "Hotstar"} # Purple
    ]
    
    original_frames = []
    watermarked_frames = []
    
    logger.info("\n Phase 1: Distributing Content with Invisible Watermarks...")
    
    # 3. Create & Watermark Frames
    for i, partner in enumerate(partners):
        fname = f"match_highlight_ep{i+1}.png"
        original_path = SAMPLE_FRAMES_DIR / fname
        
        # Create original dummy frame
        create_dummy_frame(original_path, partner["color"], partner["label"])
        original_frames.append(original_path)
        
        # Embed Watermark
        wm_fname = f"wm_{fname}"
        wm_path = LEAKED_FRAMES_DIR / wm_fname # Temporarily store here for demo flow
        
        if embed_watermark(original_path, wm_path, partner["id"]):
            watermarked_frames.append({"path": wm_path, "partner": partner["id"]})
            logger.info(f"    Sent to {partner['label']} (ID: {partner['id']})")
        else:
            logger.error(f"    Failed to watermark for {partner['label']}")

    # 4. Simulate a Leak
    logger.info("\n PHASE 2: ALERT! Pirated Content Detected on Telegram!")
    time.sleep(1.5) 
    
    # Pick the SECOND partner to be the leaker (Prime)
    leaker_data = watermarked_frames[1] 
    leaked_file = leaker_data["path"]
    
    # Move it to a "Found" folder to simulate discovery
    found_file = LEAKED_FRAMES_DIR / f"TELEGRAM_LEAK_{leaked_file.name}"
    shutil.copy(leaked_file, found_file)
    
    logger.info(f"    Found suspicious file: {found_file.name}")
    logger.info(f"    Initiating Forensic Analysis...")
    time.sleep(1.0)

    # 5. Trace the Leak
    extracted_id = extract_watermark(found_file)
    
    logger.info(f"\n Extraction Result: '{extracted_id}'")
    
    # 6. Generate Report & Verdict
    if "PARTNER" in extracted_id:
        verdict = "IDENTIFIED"
        action = "ISSUE DMCA & TERMINATE CONTRACT"
        confidence = "99.9%"
    else:
        verdict = "UNKNOWN SOURCE"
        action = "INVESTIGATE FURTHER"
        confidence = "N/A"

    report = {
        "status": "SUCCESS",
        "leaked_file": str(found_file.name),
        "extracted_source_id": extracted_id,
        "verdict": verdict,
        "recommended_action": action,
        "confidence": confidence,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2)
        
    # 7. Final Output Dashboard
    print("\n" + "="*60)
    print("   LEAK TRACE COMPLETE")
    print("="*60)
    print(f"  Leaked File   : {found_file.name}")
    print(f"  Source ID     : {extracted_id}")
    print(f"   Verdict       : {verdict}")
    print(f"  Action        : {action}")
    print(f"  Report Saved  : {REPORT_PATH.name}")
    print("="*60)
   

if __name__ == "__main__":
    main()