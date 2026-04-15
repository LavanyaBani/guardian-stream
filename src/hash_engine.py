from __future__ import annotations

import json
import logging
import os
import shutil
import tempfile
from pathlib import Path

import imagehash
from google.cloud import storage
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
KEY_PATH = ROOT / "service-account-key.json"
TEMP_DOWNLOAD_DIR = ROOT / "temp_hash_download"
HASH_DB_PATH = ROOT / "hash_database.json"

ORIGINAL_BUCKET = "guardian-original-frames-lavanya"
PIRATED_BUCKET = "guardian-sample_edited-frames-lavanya"

MATCH_THRESHOLD = 10

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def init_storage_client() -> storage.Client:
    """Load credentials from project root and return a GCS client."""
    if not KEY_PATH.exists():
        raise FileNotFoundError(f"Service account key not found: {KEY_PATH}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(KEY_PATH)
    logger.info("Credentials loaded from: %s", KEY_PATH)

    client = storage.Client.from_service_account_json(str(KEY_PATH))
    logger.info("GCS client initialized. Project: %s", client.project)
    return client


def hash_image(local_path: Path) -> str:
    """Return perceptual hash hex string for an image."""
    with Image.open(local_path) as img:
        # pHash is generally stronger for perceptual matching.
        return str(imagehash.phash(img))


def process_bucket(
    client: storage.Client,
    bucket_name: str,
    type_label: str,
    db_rows: list[dict[str, str]],
) -> None:
    """Download, hash, and index every frame blob in a bucket."""
    bucket = client.bucket(bucket_name)
    blobs = list(client.list_blobs(bucket_name))
    logger.info("Scanning bucket '%s' (%d blobs)", bucket_name, len(blobs))

    for blob in blobs:
        # Skip non-image objects if any exist.
        if not blob.name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        # Skip folder placeholders.
        if blob.name.endswith("/"):
            continue

        try:
            filename = Path(blob.name).name
            video_folder = Path(blob.name).parent.name
            local_path = TEMP_DOWNLOAD_DIR / filename

            blob.download_to_filename(str(local_path))
            frame_hash = hash_image(local_path)

            db_rows.append(
                {
                    "hash": frame_hash,
                    "path": f"{bucket_name}/{blob.name}",
                    "type": type_label,
                    "bucket_name": bucket_name,
                    "video_folder": video_folder,
                    "filename": filename,
                }
            )
        except Exception as exc:
            logger.error("Failed blob '%s/%s': %s", bucket_name, blob.name, exc)
        finally:
            try:
                local_path.unlink(missing_ok=True)
            except Exception:
                pass


def save_database(rows: list[dict[str, str]]) -> None:
    HASH_DB_PATH.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    logger.info("Saved hash database: %s (%d entries)", HASH_DB_PATH, len(rows))


def run_verification_test(client: storage.Client, rows: list[dict[str, str]]) -> None:
    """Re-hash one PIRATED frame and compare against all ORIGINAL hashes."""
    pirated_rows = [r for r in rows if r.get("type") == "PIRATED"]
    original_rows = [r for r in rows if r.get("type") == "ORIGINAL"]

    if not pirated_rows or not original_rows:
        logger.warning("Verification skipped: missing PIRATED or ORIGINAL entries.")
        return

    test_row = pirated_rows[0]
    bucket_name, blob_name = test_row["path"].split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False,
        dir=str(TEMP_DOWNLOAD_DIR),
    ) as tmp:
        temp_path = Path(tmp.name)

    try:
        blob.download_to_filename(str(temp_path))
        test_hash = imagehash.phash(Image.open(temp_path))
    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass

    best_match: dict[str, str] | None = None
    best_distance: int | None = None

    for row in original_rows:
        dist = test_hash - imagehash.hex_to_hash(row["hash"])
        if best_distance is None or dist < best_distance:
            best_distance = dist
            best_match = row

    if best_match is None or best_distance is None:
        logger.warning("Verification test could not find any ORIGINAL comparisons.")
        return

    print(
        "Testing Match: "
        f"{test_row['path']} vs {best_match['path']}. "
        f"Distance: {best_distance}. "
        f"Match Found? {'Yes' if best_distance < MATCH_THRESHOLD else 'No'}"
    )


def main() -> int:
    client = init_storage_client()
    TEMP_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    db_rows: list[dict[str, str]] = []
    try:
        process_bucket(client, ORIGINAL_BUCKET, "ORIGINAL", db_rows)
        process_bucket(client, PIRATED_BUCKET, "PIRATED", db_rows)
        save_database(db_rows)
        run_verification_test(client, db_rows)
        return 0
    finally:
        shutil.rmtree(TEMP_DOWNLOAD_DIR, ignore_errors=True)
        logger.info("Cleaned up temp folder: %s", TEMP_DOWNLOAD_DIR)


if __name__ == "__main__":
    raise SystemExit(main())
