import logging
from pathlib import Path
from stegano import lsb
import cv2
import os
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def embed_watermark(image_path: Path, output_path: Path, secret_id: str):
    """
    Embeds a hidden ID using LSB.
    CRITICAL: Forces PNG output to prevent JPEG compression from destroying the watermark.
    """
    try:
        if not image_path.exists():
            logger.error(f"Input image not found: {image_path}")
            return False

        src_str = str(image_path.resolve())
        
        # FORCE OUTPUT TO BE PNG regardless of what user asked for
        # This ensures lossless storage of the hidden bits
        final_output_path = output_path.with_suffix('.png')
        dest_str = str(final_output_path.resolve())

        logger.debug(f"Hiding data in {src_str}...")
        
        # 1. Hide the secret ID (Returns PIL Image)
        watermarked_img = lsb.hide(src_str, secret_id)
        
        # 2. Save as PNG (Lossless)
        if isinstance(watermarked_img, Image.Image):
            watermarked_img.save(dest_str, format='PNG')
        else:
            # Fallback if string path returned
            img = Image.open(watermarked_img)
            img.save(dest_str, format='PNG')

        if not os.path.exists(dest_str):
            raise Exception("Output file was not created.")

        logger.info(f"🔒 Successfully embedded ID '{secret_id}' into {final_output_path.name}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to embed watermark: {e}")
        return False

def extract_watermark(image_path: Path) -> str:
    """Extracts the hidden ID."""
    try:
        if not image_path.exists():
            return "ERROR: File not found"

        # Ensure we are reading the PNG version if possible
        # If user passes .jpg, we try anyway, but it likely failed at save step
        secret_id = lsb.reveal(str(image_path.resolve()))
        
        if secret_id:
            logger.info(f"🔓 Extracted ID: '{secret_id}' from {image_path.name}")
            return secret_id
        else:
            return "NO_WATERMARK_FOUND"

    except Exception as e:
        err_msg = str(e)
        if "index out of range" in err_msg:
            return "WATERMARK_CORRUPTED: Likely saved as JPG (use PNG!)"
        return f"WATERMARK_CORRUPTED: {err_msg}"

if __name__ == "__main__":
    print(" Running Watermark Engine Self-Test (PNG Fix)...")
    
    # Create dummy image using PIL (RGB)
    test_img = Path("test_dummy_frame.png").resolve() # Start with PNG
    img = Image.new('RGB', (100, 100), color=(0, 0, 255)) 
    img.save(str(test_img), format='PNG')
    
    output_img = Path("test_dummy_watermarked.png").resolve() # Output MUST be PNG
    secret = "DISTRIBUTOR_ID_992"
    
    # Run Test
    if embed_watermark(test_img, output_img, secret):
        result = extract_watermark(output_img)
        if result == secret:
            print(f"✅ TEST PASSED: Embedded & Extracted '{secret}' correctly!")
        else:
            print(f"❌ FAIL: Expected '{secret}', got '{result}'")
    else:
        print("❌ FAIL: Embedding process failed.")
        
    # Cleanup

    if test_img.exists(): 
        test_img.unlink()
        print(f" Cleaned up: {test_img.name}")
        
    if output_img.exists(): 
        output_img.unlink()  # Fixed: was deleting test_img again by mistake
        print(f"Cleaned up: {output_img.name}")
        
    print("✅ All tests complete and cleaned up.")