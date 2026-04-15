from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


INPUT_DIR = Path("data/original/real_sports")
OUTPUT_DIR = Path("data/sample_edited/edited_real")

UPSIDE_DOWN_FILTER = "hflip,vflip"
HIGH_CONTRAST_FILTER = "eq=contrast=2.0:saturation=2.0"


def _check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def _safe_unlink(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def _valid_output(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def _run_ffmpeg(input_path: Path, output_path: Path, vf_filter: str) -> tuple[bool, str]:
    """
    Run ffmpeg with a strong default encode profile.
    Returns (success, stderr_excerpt).
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(input_path),
        "-vf",
        vf_filter,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        str(output_path),
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return False, (proc.stderr or "").strip()[:3000]
    if not _valid_output(output_path):
        return False, "Output file missing or empty after ffmpeg completed."
    return True, ""


def main() -> int:
    if not _check_ffmpeg():
        print("Error: ffmpeg not found in PATH.")
        return 1

    if not INPUT_DIR.exists():
        print(f"Error: input folder not found: {INPUT_DIR}")
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    videos = sorted(p for p in INPUT_DIR.iterdir() if p.is_file() and p.suffix.lower() == ".mp4")
    if not videos:
        print(f"No .mp4 files found in {INPUT_DIR}")
        return 0

    total_created = 0
    total_failed = 0

    for video in videos:
        base = video.stem
        variants = [
            (OUTPUT_DIR / f"{base}_UPSIDE_DOWN.mp4", UPSIDE_DOWN_FILTER),
            (OUTPUT_DIR / f"{base}_HIGH_CONTRAST.mp4", HIGH_CONTRAST_FILTER),
        ]

        for output_path, vf_filter in variants:
            print(f"Creating {output_path.name} from {video.name}")
            _safe_unlink(output_path)

            try:
                ok, err = _run_ffmpeg(video, output_path, vf_filter)
            except Exception as exc:
                ok, err = False, str(exc)

            if ok:
                print(f"  OK: {output_path.name}")
                total_created += 1
            else:
                print(f"  FAILED: {output_path.name}")
                if err:
                    print(f"  Reason: {err}")
                total_failed += 1
                _safe_unlink(output_path)

    print(f"Done. Created: {total_created}, Failed: {total_failed}, Output: {OUTPUT_DIR}")
    return 0 if total_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())