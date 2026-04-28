from __future__ import annotations

import json
import logging
import os
import random
from pathlib import Path

from google.cloud import storage
from google.cloud import vision

ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = ROOT / "service-account-key.json"
HASH_DB_PATH = ROOT / "hash_database.json"
REPORT_PATH = ROOT / "vision_forensics_report.json"

ORIGINAL_BUCKET = "guardian-original-frames-lavanya"
PIRATED_BUCKET = "guardian-sample_edited-frames-lavanya"

AI_KEYWORDS = ["Sora", "Runway", "TikTok", "AI", "Generated", "Deepfake"]
PIRATED_HINTS = ["high_contrast", "upside_down", "deepfake"]
SAMPLE_SIZE = 5

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def init_clients() -> tuple[storage.Client, vision.ImageAnnotatorClient]:
    """Load credentials from root and create GCS + Vision clients."""
    if not KEY_PATH.exists():
        raise FileNotFoundError(f"Service account key not found: {KEY_PATH}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(KEY_PATH)
    logger.info("Credentials loaded from: %s", KEY_PATH)

    storage_client = storage.Client.from_service_account_json(str(KEY_PATH))
    vision_client = vision.ImageAnnotatorClient.from_service_account_file(str(KEY_PATH))
    return storage_client, vision_client


def load_hash_database() -> list[dict[str, str]]:
    if not HASH_DB_PATH.exists():
        raise FileNotFoundError(f"hash_database.json not found at: {HASH_DB_PATH}")

    raw = HASH_DB_PATH.read_text(encoding="utf-8")
    rows = json.loads(raw)
    if not isinstance(rows, list):
        raise ValueError("hash_database.json must contain a JSON list")
    return rows


def _is_relevant_pirated(entry: dict[str, str]) -> bool:
    if entry.get("type") != "PIRATED":
        return False
    path = entry.get("path", "").lower()
    return any(hint in path for hint in PIRATED_HINTS)


def sample_pirated_frames(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    candidates = [row for row in rows if _is_relevant_pirated(row)]
    if not candidates:
        return []

    random.seed(42)  # stable sample for repeatable hackathon demos
    k = min(SAMPLE_SIZE, len(candidates))
    return random.sample(candidates, k=k)


def parse_bucket_blob(path_value: str) -> tuple[str, str]:
    """
    Parse 'bucket/blob/path.jpg' (as stored in hash_database.json).
    """
    if "/" not in path_value:
        raise ValueError(f"Invalid path format in database: {path_value}")
    bucket_name, blob_name = path_value.split("/", 1)
    return bucket_name, blob_name


def vision_analyze_bytes(
    vision_client: vision.ImageAnnotatorClient, image_bytes: bytes
) -> tuple[list[str], list[str], list[str], str | None]:
    image = vision.Image(content=image_bytes)
    response = vision_client.annotate_image(
        request={
            "image": image,
            "features": [
                {"type_": vision.Feature.Type.LOGO_DETECTION},
                {"type_": vision.Feature.Type.TEXT_DETECTION},
                {"type_": vision.Feature.Type.LABEL_DETECTION},
            ],
        }
    )

    if response.error.message:
        raise RuntimeError(response.error.message)

    logos = [ann.description for ann in (response.logo_annotations or []) if ann.description]

    text_detected: list[str] = []
    if response.text_annotations:
        # First element is often the full text block.
        text_detected = [ann.description for ann in response.text_annotations[:5] if ann.description]

    labels = [ann.description for ann in (response.label_annotations or []) if ann.description][:3]

    joined_text = " ".join(text_detected).lower()
    warning: str | None = None
    for kw in AI_KEYWORDS:
        if kw.lower() in joined_text:
            warning = f"Detected keyword: {kw}"
            break

    return labels, logos, text_detected, warning


def analyze_frame(
    storage_client: storage.Client,
    vision_client: vision.ImageAnnotatorClient,
    db_entry: dict[str, str],
) -> dict[str, object]:
    bucket_name, blob_name = parse_bucket_blob(db_entry.get("path", ""))
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    image_bytes = blob.download_as_bytes()
    labels, logos, text_detected, warning = vision_analyze_bytes(vision_client, image_bytes)

    filename = Path(blob_name).name
    result = {
        "bucket_name": bucket_name,
        "blob_name": blob_name,
        "filename": filename,
        "labels": labels,
        "logos": logos,
        "text_detected": text_detected,
        "ai_warning": warning,
    }

    print(f" Analyzing: {filename}")
    print(f" Labels: {labels if labels else []}")
    print(f" Logos: {logos if logos else []}")
    print(f" Text Detected: {text_detected if text_detected else []}")
    print(f" AI Warning: {warning if warning else 'None'}")
    print("-" * 70)
    return result


def main() -> int:
    storage_client, vision_client = init_clients()
    db_rows = load_hash_database()
    sampled = sample_pirated_frames(db_rows)

    if not sampled:
        logger.warning("No matching PIRATED frames found for sampling.")
        REPORT_PATH.write_text(json.dumps([], indent=2), encoding="utf-8")
        return 0

    logger.info("Selected %d PIRATED frame(s) for Vision analysis.", len(sampled))

    report: list[dict[str, object]] = []
    for entry in sampled:
        try:
            # Safety check to keep analysis scoped to intended buckets.
            path_value = entry.get("path", "")
            if not path_value.startswith((PIRATED_BUCKET + "/", ORIGINAL_BUCKET + "/")):
                logger.warning("Skipping unknown bucket path: %s", path_value)
                continue
            report.append(analyze_frame(storage_client, vision_client, entry))
        except Exception as exc:
            logger.error("Failed frame analysis for %s: %s", entry.get("path", ""), exc)

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Saved report: %s", REPORT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
