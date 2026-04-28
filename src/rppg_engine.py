import logging
import cv2
import numpy as np
from pathlib import Path
from scipy.signal import find_peaks
from scipy.fft import fft

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def extract_face_roi(frame: np.ndarray) -> np.ndarray:
    """Extracts the face region from a frame using OpenCV's Haar Cascade."""
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            return frame[y:y+h, x:x+w]
        return None
    except Exception as e:
        logger.debug(f"Face detection failed: {e}")
        return None

def extract_green_channel_signal(frames: list) -> np.ndarray:
    """Extracts the average green channel intensity from each frame."""
    green_signal = []
    for frame in frames:
        face = extract_face_roi(frame)
        if face is not None:
            green_mean = np.mean(face[:, :, 1])  # Channel 1 is Green in BGR
            green_signal.append(green_mean)
        else:
            green_mean = np.mean(frame[:, :, 1])
            green_signal.append(green_mean)
    return np.array(green_signal)

def detrend_signal(signal: np.ndarray, lambda_param: int = 100) -> np.ndarray:
    """Removes trends from the signal using smoothness priors."""
    try:
        from scipy import sparse
        L = len(signal)
        H = np.identity(L)
        D = np.diff(np.eye(L), n=2, axis=0)
        B = np.linalg.inv(H + (lambda_param ** 2) * D.T @ D)
        trend = B @ signal
        return signal - trend
    except Exception:
        # Fallback: simple moving average detrend
        kernel = np.ones(30) / 30
        trend = np.convolve(signal, kernel, mode='same')
        return signal - trend

def calculate_pulse_metrics(signal: np.ndarray, fps: float = 30.0) -> dict:
    """Analyzes the signal for pulse-like characteristics."""
    # Detrend and normalize
    detrended = detrend_signal(signal)
    if np.std(detrended) > 0:
        detrended = (detrended - np.mean(detrended)) / np.std(detrended)
    
    # Frequency analysis
    freqs = np.fft.fftfreq(len(detrended), 1/fps)
    spectrum = np.abs(fft(detrended))
    
    # Focus on heart rate range: 0.7 Hz to 4 Hz (42-240 BPM)
    mask = (freqs >= 0.7) & (freqs <= 4.0)
    relevant_freqs = freqs[mask]
    relevant_spectrum = spectrum[mask]
    
    if len(relevant_spectrum) == 0:
        return {
            "pulse_detected": False,
            "confidence": 0.0,
            "estimated_bpm": 0,
            "reasoning": "No signal in heart rate frequency range"
        }
    
    # Find peak frequency
    peak_idx = np.argmax(relevant_spectrum)
    peak_freq = relevant_freqs[peak_idx]
    estimated_bpm = peak_freq * 60
    
    # Calculate SNR
    signal_power = relevant_spectrum[peak_idx]
    noise_power = np.median(relevant_spectrum) + 1e-10
    snr = 10 * np.log10(signal_power / noise_power)
    
    # Peak detection in time domain
    peaks, _ = find_peaks(detrended, distance=fps*0.3, prominence=0.1)
    
    # Decision logic
    if len(peaks) >= 3 and snr > 3 and 40 <= estimated_bpm <= 180:
        confidence = min(0.95, (snr / 10) * 0.5 + (len(peaks) / max(len(detrended), 1)) * 0.5)
        return {
            "pulse_detected": True,
            "confidence": confidence,
            "estimated_bpm": round(estimated_bpm, 1),
            "snr_db": round(snr, 2),
            "num_peaks": len(peaks),
            "reasoning": f"Physiological pulse detected at {estimated_bpm:.0f} BPM (SNR: {snr:.1f} dB)"
        }
    else:
        return {
            "pulse_detected": False,
            "confidence": 0.0,
            "estimated_bpm": round(estimated_bpm, 1),
            "snr_db": round(snr, 2),
            "num_peaks": len(peaks),
            "reasoning": f"No consistent pulse pattern found (SNR: {snr:.1f} dB, peaks: {len(peaks)}, BPM: {estimated_bpm:.0f})"
        }

def analyze_video_for_pulse(video_path: Path, max_frames: int = 300) -> dict:
    """
    Main function: Analyzes a video for physiological pulse signals.
    
    Returns dict with verdict, confidence, estimated_bpm, reasoning.
    """
    logger.info(f" Analyzing video for pulse: {video_path.name}")
    
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return {
                "verdict": "ANALYSIS_FAILED",
                "confidence": 0.0,
                "reasoning": "Could not open video file"
            }
        
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frames = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret or frame_count >= max_frames:
                break
            
            face = extract_face_roi(frame)
            if face is not None and face.shape[0] > 50 and face.shape[1] > 50:
                frames.append(frame)
            frame_count += 1
        
        cap.release()
        
        if len(frames) < 30:
            return {
                "verdict": "INSUFFICIENT_DATA",
                "confidence": 0.0,
                "reasoning": f"Insufficient frames with detectable faces ({len(frames)} frames)"
            }
        
        logger.info(f" Extracted {len(frames)} frames with faces")
        
        # Extract green channel signal
        green_signal = extract_green_channel_signal(frames)
        
        # Analyze for pulse
        metrics = calculate_pulse_metrics(green_signal, fps)
        
        # Return structured result with verdict key
        if metrics["pulse_detected"]:
            logger.info(f" PULSE DETECTED: {metrics['reasoning']}")
            return {
                "verdict": "REAL_PERSON",
                "confidence": metrics["confidence"],
                "estimated_bpm": metrics["estimated_bpm"],
                "reasoning": metrics["reasoning"],
                "snr_db": metrics["snr_db"]
            }
        else:
            logger.warning(f" NO PULSE DETECTED: {metrics['reasoning']}")
            return {
                "verdict": "POSSIBLE_DEEPFAKE",
                "confidence": 0.85,
                "reasoning": f"No physiological pulse detected. {metrics['reasoning']}",
                "snr_db": metrics.get("snr_db", 0)
            }
    
    except Exception as e:
        logger.error(f" rPPG analysis failed: {e}")
        return {
            "verdict": "ANALYSIS_FAILED",
            "confidence": 0.0,
            "reasoning": f"Error: {str(e)}"
        }

if __name__ == "__main__":
    print(" rPPG Engine Self-Test")
    import sys
    if len(sys.argv) > 1:
        video_path = Path(sys.argv[1])
        result = analyze_video_for_pulse(video_path)
        print(f"\n Result: {result}")
    else:
        print("Usage: python rppg_engine.py path/to/video.mp4")