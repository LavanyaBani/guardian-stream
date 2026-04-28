# **Guardian-Stream**
GuardianStream is a production-grade, multi-modal forensic analysis platform designed to protect sports broadcasters from deepfakes, piracy, and misinformation. Our system employs seven distinct forensic engines that work in concert to verify video authenticity and trace unauthorized content distribution in real-time.

## **Key Capabilities**--
Biological Authentication,  Leak Source Identification, Deepfake Detection, Real-Time Analysis,  Legal Evidence


##  Installation

### **Prerequisites**
Python 3.11 or higher
FFmpeg (for audio extraction)
Git
### Step 1: Clone Repository
git clone https://github.com/yourusername/guardian-stream.git
cd guardian-stream

### Step 2: Create Virtual Environment
 Windows
python -m venv .venv
.venv\Scripts\activate

 macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

### Step 3: Install Python Dependencies
pip install -r requirements.txt

### **Step 4: Install FFmpeg**
Windows:  Download from https://ffmpeg.org/download.html --> Add to system PATH
macOS: brew install ffmpeg
Linux: sudo apt-get install ffmpeg

### Step 5: Configure Google Gemini API
GOOGLE_API_KEY=your_api_key_here

### Step 6: Verify Installation
 Test rPPG engine
python src/rppg_engine.py

 Test lip-sync engine
python src/lip_sync_engine.py videos/novak_interview_real.mp4

 Test news fetcher
python test_news_fetch.py

##  Usage & Running Modes
### Mode 1: Interactive Analysis (Recommended)
Analyze videos with full forensic pipeline:
  python src/gemini_intelligence.py --interactive

Interactive Prompt: Example
  Enter video file path (or press Enter for demo clips): videos/novak_interview_real.mp4
  Video type:
   1. Interview/Close-up (enables rPPG + Lip-Sync)
   2. Sports/Wide-shot (skips rPPG + Lip-Sync)
   Choose (1 or 2, default=2): 1

  Context: Novak Djokovic post match conference

Output: INFO REAL MODE ENABLED - Will analyze actual video files
INFO Video: videos/novak_interview_real.mp4
INFO Initializing GenAI Client with Stable API (v1)...
INFO Loaded 5 entries from vision report
INFO Transcribing first 15s of novak_interview_real.mp4...
INFO [REAL] Whisper transcript: "I don't know what I can say to them..."
INFO Running Semantic Triangulation...
INFO PULSE DETECTED: Physiological pulse at 71 BPM
INFO Verdict: AUTHENTIC (Confidence: 93%)
INFO Analysis Complete! Saved to gemini_intelligence_report.json

### Mode 2: Piracy Simulation
Simulate leak detection and trace source:
  python src/simulate_leak_trace.py

Output:
INFO Starting GuardianStream Piracy Detection & Trace Demo
INFO Phase 1: Distributing Content with Invisible Watermarks...
INFO Successfully embedded ID 'PARTNER_A_NETFLIX' into wm_match_ep1.png
INFO Successfully embedded ID 'PARTNER_B_PRIME' into wm_match_ep2.png
INFO Successfully embedded ID 'PARTNER_C_HOTSTAR' into wm_match_ep3.png
INFO PHASE 2: ALERT! Pirated Content Detected on Telegram!
INFO Found suspicious file: TELEGRAM_LEAK_wm_match_ep2.png
INFO Initiating Forensic Analysis...
INFO Extracted ID: 'PARTNER_B_PRIME' from TELEGRAM_LEAK...
Extraction Result: 'PARTNER_B_PRIME'

==================== LEAK TRACE COMPLETE ====================
Leaked File     : TELEGRAM_LEAK_wm_match_ep2.png
Source ID       : PARTNER_B_PRIME
Verdict         : IDENTIFIED
Action          : ISSUE DMCA & TERMINATE CONTRACT
Report Saved    : leak_trace_report.json
==============================================================

### Mode 3: Individual Engine Testing
Test specific forensic engines:
 Test rPPG engine
  python src/rppg_engine.py videos/novak_interview_real.mp4

 Test lip-sync engine
  python src/lip_sync_engine.py videos/novak_interview_real.mp4 150

 Test vision forensics
  python src/vision_forensics.py videos/novak_interview_real.mp4

 Test news fetcher
  python test_news_fetch.py "Novak Djokovic Australian Open"

 Test semantic dissonance
  python test_dissonance_standalone.py
 

## The Problem
The sports broadcasting industry faces unprecedented threats: Deepfake Interviews, Broadcast Piracy, Misinformation, No Biological Proof, No Legal Evidence

**GuardianStream solves all five gaps with a unified 7-layer forensic platform**

## **Seven-Layer Forensic Engine**
### **Layer 1: Perceptual Hash (pHash)**
Purpose: Detect unauthorized copies and modified versions of broadcast content.
How It Works:
Convert video frame to grayscale
Resize to 32×32 pixels (standardization)
Apply Discrete Cosine Transform (DCT)
Extract low-frequency components (top-left 8×8)
Calculate median value
Generate 64-bit hash: 1 if pixel > median, 0 otherwise
Compare hashes using Hamming distance (threshold < 10 = match)
Technical Specs:
Hash Size: 64 bits
Processing Speed: ~50ms per frame
Robustness: Survives compression, resizing, color changes
Accuracy: 98% for duplicate detection
File: src/hash_engine.py

### **Layer 2: Vision AI + OCR**
Purpose: Extract visual context and on-screen text for verification.
Components:
A. OCR (Optical Character Recognition)
Engine: Tesseract OCR / EasyOCR
Preprocessing: Contrast enhancement, denoising
Text detection: CRAFT or DBNet
Recognition: CTC decoding
Output: Text + bounding boxes + confidence
B. Vision AI (Scene Understanding)
Model: CLIP / ViT / ResNet
Tasks: Object detection, scene classification, brand recognition

Output Example:
{
  "text_overlay": [
    {"text": "LIVE", "confidence": 0.98, "bbox": [10, 10, 50, 30]},
    {"text": "AO 2024", "confidence": 0.95, "bbox": [100, 10, 200, 30]}
  ],
  "scene_labels": ["tennis_court", "press_conference", "athlete"],
  "detected_objects": [
    {"class": "person", "confidence": 0.99},
    {"class": "microphone", "confidence": 0.87},
    {"class": "Rolex_logo", "confidence": 0.92}
  ]
}
File: src/vision_forensics.py

### **Layer 3: Live News Verification**
Purpose: Ground video claims in reality by cross-referencing live news sources.
Workflow:
Extract context from video (OCR + Vision AI)
Generate search query (e.g., "Novak Djokovic Australian Open 2024")
Query Google News RSS API
Filter results by trusted sources (ESPN, BBC, Reuters, ICC)
Calculate credibility score (0-100%)
File: src/news_fetcher.py

### **Layer 4: Semantic Dissonance Detection**
Purpose: Detect misleading context by comparing video content, audio transcript, and news.
Triangulation Algorithm:
Year/Date Mismatch: OCR text ("2019 World Cup") vs audio claims ("2024 scandal")
Claim Contradiction: Audio claims contradict verified news
Player/Event Mismatch: Video shows Player A but audio mentions Player B
File: src/action_engine.py, test_dissonance_standalone.py

### **Layer 5: rPPG Biological Detection**
Purpose: Detect real human heartbeat in video frames to prove biological authenticity.
The Science:
Remote Photoplethysmography (rPPG) measures subtle color changes in facial skin caused by blood flow. When the heart pumps, facial skin reflects slightly more red light. This change is imperceptible to humans but detectable by computer vision.

Technical Pipeline:
1. Face Detection & Tracking (MediaPipe Face Mesh)
2. Extract forehead ROI (best for rPPG)
3. Color Signal Extraction (RGB channels over time)
4. Signal Preprocessing (Detrend + Normalize)
5. CHROM Method (Color space transformation)
6. Bandpass Filter (0.7-4.0 Hz = 42-240 BPM)
7. Peak Detection (SciPy signal.find_peaks)
8. Calculate BPM (60 / avg_peak_interval)
9. SNR Calculation (Signal quality metric)
10. Decision: Real human if BPM 40-180 AND SNR > 3dB

File: src/rppg_engine.py

### **Layer 6: Lip-Sync Forensics**
Purpose: Detect audio-video manipulation by correlating mouth movements with audio energy.

Technical Pipeline:
1. Extract Audio Energy (Librosa RMS)
2. Detect Mouth Regions (MediaPipe 37 landmarks)
3. Calculate Mouth Opening (Threshold-based)
4. Align Signals (Match video FPS to audio hop length)
5. Calculate Pearson Correlation
6. Decision: >0.4 = MATCH, <0.2 = MISMATCH

File: src/lip_sync_engine.py

### **Layer 7: Steganography Watermark Extraction**
Purpose: Extract hidden forensic watermarks to trace content leaks to source partners.
Watermarking Scheme:
Embedding (Done by Broadcaster):
LSB (Least Significant Bit) steganography in blue channel
Partner ID encoded as binary (e.g., "PARTNER_B_PRIME")
Embedded across multiple frames for robustness

Extraction (Forensic Analysis):
1. Read video frame
2. Extract LSB from blue channel
3. Reconstruct binary string
4. Convert to ASCII text
5. Pattern match partner ID (regex: PARTNER_[A-Z]+)
6. Lookup partner in database
7. Generate DMCA evidence

Leak Trace Workflow:
Leaked File: TELEGRAM_LEAK_wm_match.mp4
Extracted Watermark: "PARTNER_B_PRIME"
Source: Amazon Prime (Global, Premium Tier)
Confidence: 98.5%
Action: Issue DMCA takedown notice to Amazon Prime

File: src/watermark_engine.py, src/simulate_leak_trace.py


## ** Tech Stack**

### **Backend (Python 3.11+)**
<img width="421" height="271" alt="image" src="https://github.com/user-attachments/assets/faf1cda1-cf9d-4b71-98dd-65cd192289c8" />

### **Frontend**
HTML/CSS/JS(Static Pages)
Next.js, TyspeScript, Tailwind CSS (Future Scope)

## Reports Generated
GuardianStream generates comprehensive forensic reports for legal and analytical use.

### 1. Gemini Intelligence Report (gemini_intelligence_report.json)
Generated by: src/gemini_intelligence.py
Contents:

[
  {
    "clip_tag": "Custom_Video_Analysis",
    "context": "Novak Djokovic post match conference",
    "video_path": "videos/novak_interview_real.mp4",
    "ai_verdict": {
      "verdict": "AUTHENTIC",
      "reasoning": "All forensic signals align with authentic content",
      "confidence": 0.93
    },
    "rppg_verdict": {
      "verdict": "REAL_PERSON",
      "estimated_bpm": 71,
      "snr_db": 5.6,
      "confidence": 0.93
    },
    "lip_sync_verdict": {
      "verdict": "AUDIO_VIDEO_MATCH",
      "correlation": 0.67,
      "confidence": 0.82
    },
    "news_credibility_pct": 100,
    "dissonance_verdict": "CONSISTENT",
    "final_confidence_pct": 93,
    "timestamp": "2026-04-29T19:45:32"
  }
]

### 2. Leak Trace Report (leak_trace_report.json)
Generated by: src/simulate_leak_trace.py
Contents:

{
  "leaked_file": "TELEGRAM_LEAK_wm_match_ep2.png",
  "source_id": "PARTNER_B_PRIME",
  "partner_name": "Amazon Prime",
  "region": "Global",
  "tier": "Premium",
  "verdict": "IDENTIFIED",
  "confidence": 98.5,
  "extraction_method": "Steganography LSB",
  "timestamp": "2026-04-29T18:43:09",
  "action": "ISSUE DMCA & TERMINATE CONTRACT"
}

### 3. Vision Forensics Report (vision_forensics_report.json)
Generated by: src/vision_forensics.py
Contents:

{
  "video_path": "videos/novak_interview_real.mp4",
  "ocr_results": [
    {"text": "AO 2024", "confidence": 0.95, "bbox": [100, 10, 200, 30]},
    {"text": "LIVE", "confidence": 0.98, "bbox": [10, 10, 50, 30]}
  ],
  "scene_labels": ["tennis_court", "press_conference", "athlete"],
  "detected_objects": [
    {"class": "person", "confidence": 0.99},
    {"class": "microphone", "confidence": 0.87},
    {"class": "Rolex_logo", "confidence": 0.92}
  ],
  "timestamp": "2026-04-29T19:30:15"
}

### 4. DMCA Takedown Notice (DMCA_Test_Clip_01.txt)
Generated by: src/action_engine.py
Contents:

DIGITAL MILLENNIUM COPYRIGHT ACT
TAKEDOWN NOTICE

To: Telegram Legal Department
From: GuardianStream Broadcasting Security Team
Re: Unauthorized Distribution of Sports Broadcast Assets
Date: 2026-04-29

EVIDENCE:
- Watermark ID: PARTNER_B_PRIME
- Extraction Method: Steganography LSB
- Confidence: 98.5%
- Leaked File: TELEGRAM_LEAK_wm_match_ep2.png
- Timestamp: 2026-04-29T18:43:09

FORENSIC ANALYSIS:
- pHash Match: Confirmed (Hamming distance: 3)
- rPPG Verdict: REAL_PERSON (71 BPM)
- Lip-Sync Correlation: 0.67

LEGAL BASIS: DMCA §512(c) - Notice and Takedown

ACTION REQUESTED: Immediate removal of infringing content

[Digital Signature]
GuardianStream Security Team


### 5. Propagation Network Graph (propagation_graph.png)
Generated by: src/action_engine.py
Description: Visual representation of how leaked content spreads across platforms (Twitter → YouTube → Telegram → Torrent sites).

### 6. Terminal Output Logs
All analysis sessions generate real-time terminal logs showing:
Engine initialization
Frame processing progress
Intermediate results (BPM, correlation, credibility)
Final verdict with confidence

Example: 
INFO Starting GuardianStream Analysis...
INFO Video: novak_interview_real.mp4
INFO Context: Novak Djokovic post match conference
INFO Loading Whisper model (small)...
INFO Transcribing first 15s of video...
✅ Transcript: "I don't know what I can say to them..."
INFO Running rPPG Analysis (Close-up detected)...
✅ Extracted 228 frames with faces
✅ PULSE DETECTED: Physiological pulse at 71 BPM
✅ rPPG Result: REAL_PERSON
INFO Running Lip-Sync Analysis...
✅ Lip-Sync Result: AUDIO_VIDEO_MATCH
INFO Verdict: AUTHENTIC (Confidence: 93%)
✅ Analysis Complete! Report saved.





