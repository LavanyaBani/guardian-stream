import logging
import whisper
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Lazy-load model
_model = None

def transcribe_audio(video_path: Path, duration_sec: int = 15) -> str:
    """
    Extracts and transcribes first N seconds of audio using Whisper.
    Returns the transcript text.
    """
    global _model
    
    try:
        # Lazy-load model
        if _model is None:
            logger.info(" Loading Whisper model (small)...")
            _model = whisper.load_model("small")
        
        logger.info(f" Transcribing first {duration_sec}s of {video_path.name}...")
        
      
        result = _model.transcribe(
            str(video_path),
            language="en",
            task="transcribe",
            fp16=False  
        )
        
        # Get transcript 
        transcript = result["text"].strip()
        
        #  truncate to first ~100 chars for demo display
        if len(transcript) > 100:
            display_text = transcript[:100] + "..."
        else:
            display_text = transcript
            
        logger.info(f" Transcript: '{display_text}'")
        return transcript
        
    except Exception as e:
        logger.error(f" Transcription failed: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        video = Path(sys.argv[1])
        print(f" Testing Whisper on: {video.name}")
        result = transcribe_audio(video)
        print(f"\n Result: {result}")
    else:
        print("Usage: python audio_transcriber.py path/to/video.mp4")