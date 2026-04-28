# **Guardian-Stream**
GuardianStream is a production-grade, multi-modal forensic analysis platform designed to protect sports broadcasters from deepfakes, piracy, and misinformation. Our system employs seven distinct forensic engines that work in concert to verify video authenticity and trace unauthorized content distribution in real-time.

## **Key Capabilities**--
Biological Authentication,  Leak Source Identification, Deepfake Detection, Real-Time Analysis,  Legal Evidence



## The Problem
The sports broadcasting industry faces unprecedented threats: Deepfake Interviews, Broadcast Piracy, Misinformation, No Biological Proof, No Legal Evidence

**GuardianStream solves all five gaps with a unified 7-layer forensic platform**

## **Seven-Layer Forensic Engine**
### **Layer 1: Perceptual Hash (pHash)**
Purpose: Detect unauthorized copies and modified versions of broadcast content.<br><br>
How It Works:<br>
Convert video frame to grayscale<br>
Resize to 32×32 pixels (standardization)<br>
Apply Discrete Cosine Transform (DCT)<br>
Extract low-frequency components (top-left 8×8)<br>
Calculate median value<br>
Generate 64-bit hash: 1 if pixel > median, 0 otherwise<br>
Compare hashes using Hamming distance (threshold < 10 = match)<br>
Technical Specs:<br>
Hash Size: 64 bits<br>
Processing Speed: ~50ms per frame<br>
Robustness: Survives compression, resizing, color changes<br>
Accuracy: 98% for duplicate detection<br>
File: src/hash_engine.py<br>

### **Layer 2: Vision AI + OCR**
Purpose: Extract visual context and on-screen text for verification.<br><br>
Components:<br>
A. OCR (Optical Character Recognition)<br>
Engine: Tesseract OCR / EasyOCR<br>
Preprocessing: Contrast enhancement, denoising<br>
Text detection: CRAFT or DBNet<br>
Recognition: CTC decoding<br>
Output: Text + bounding boxes + confidence<br>
B. Vision AI (Scene Understanding)<br>
Model: CLIP / ViT / ResNet<br>
Tasks: Object detection, scene classification, brand recognition<br><br>

Output Example:<br>
{<br>
  "text_overlay": [<br>
    {"text": "LIVE", "confidence": 0.98, "bbox": [10, 10, 50, 30]},<br>
    {"text": "AO 2024", "confidence": 0.95, "bbox": [100, 10, 200, 30]}<br>
  ],<br>
  "scene_labels": ["tennis_court", "press_conference", "athlete"],<br>
  "detected_objects": [<br>
    {"class": "person", "confidence": 0.99},<br>
    {"class": "microphone", "confidence": 0.87},<br>
    {"class": "Rolex_logo", "confidence": 0.92}<br>
  ]<br>
}<br>
File: src/vision_forensics.py<br>

### **Layer 3: Live News Verification**
Purpose: Ground video claims in reality by cross-referencing live news sources.<br>
Workflow:<br>
Extract context from video (OCR + Vision AI)<br>
Generate search query (e.g., "Novak Djokovic Australian Open 2024")<br>
Query Google News RSS API<br>
Filter results by trusted sources (ESPN, BBC, Reuters, ICC)<br>
Calculate credibility score (0-100%)<br>
File: src/news_fetcher.py<br>

### **Layer 4: Semantic Dissonance Detection**v
Purpose: Detect misleading context by comparing video content, audio transcript, and news.<br>
Triangulation Algorithm:<br>
Year/Date Mismatch: OCR text ("2019 World Cup") vs audio claims ("2024 scandal")<br>
Claim Contradiction: Audio claims contradict verified news<br>
Player/Event Mismatch: Video shows Player A but audio mentions Player B<br>
File: src/action_engine.py, test_dissonance_standalone.py<br>

### **Layer 5: rPPG Biological Detection**
Purpose: Detect real human heartbeat in video frames to prove biological authenticity.<br>
The Science:<br>
Remote Photoplethysmography (rPPG) measures subtle color changes in facial skin caused by blood flow. When the heart pumps, facial skin reflects slightly more red light. This change is imperceptible to humans but detectable by computer vision.<br>

Technical Pipeline:<br>
1. Face Detection & Tracking (MediaPipe Face Mesh)<br>
2. Extract forehead ROI (best for rPPG)<br>
3. Color Signal Extraction (RGB channels over time)<br>
4. Signal Preprocessing (Detrend + Normalize)<br>
5. CHROM Method (Color space transformation)<br>
6. Bandpass Filter (0.7-4.0 Hz = 42-240 BPM)<br>
7. Peak Detection (SciPy signal.find_peaks)<br>
8. Calculate BPM (60 / avg_peak_interval)<br>
9. SNR Calculation (Signal quality metric)<br>
10. Decision: Real human if BPM 40-180 AND SNR > 3dB<br><br>

File: src/rppg_engine.py

### **Layer 6: Lip-Sync Forensics**
Purpose: Detect audio-video manipulation by correlating mouth movements with audio energy.<br><br>

Technical Pipeline:<br>
1. Extract Audio Energy (Librosa RMS)<br>
2. Detect Mouth Regions (MediaPipe 37 landmarks)<br>
3. Calculate Mouth Opening (Threshold-based)<br>
4. Align Signals (Match video FPS to audio hop length)<br>
5. Calculate Pearson Correlation<br>
6. Decision: >0.4 = MATCH, <0.2 = MISMATCH<br><br>

File: src/lip_sync_engine.py

### **Layer 7: Steganography Watermark Extraction**
Purpose: Extract hidden forensic watermarks to trace content leaks to source partners.<br>
Watermarking Scheme:<br>
Embedding (Done by Broadcaster):<br>
LSB (Least Significant Bit) steganography in blue channel<br>
Partner ID encoded as binary (e.g., "PARTNER_B_PRIME")<br>
Embedded across multiple frames for robustness<br><br>

Extraction (Forensic Analysis):<br>
1. Read video frame<br>
2. Extract LSB from blue channel<br>
3. Reconstruct binary string<br>
4. Convert to ASCII text<br>
5. Pattern match partner ID (regex: PARTNER_[A-Z]+)<br>
6. Lookup partner in database<br>
7. Generate DMCA evidence<br><br>

Leak Trace Workflow:<br>
Leaked File: TELEGRAM_LEAK_wm_match.mp4<br>
Extracted Watermark: "PARTNER_B_PRIME"<br>
Source: Amazon Prime (Global, Premium Tier)<br>
Confidence: 98.5%<br>
Action: Issue DMCA takedown notice to Amazon Prime<br><br>

File: src/watermark_engine.py, src/simulate_leak_trace.py<br>


##  Installation

### **Prerequisites**
Python 3.11 or higher<br>
FFmpeg (for audio extraction)<br>
Git<br>
### Step 1: Clone Repository
git clone https://github.com/yourusername/guardian-stream.git<br>
cd guardian-stream<br>

### Step 2: Create Virtual Environment
 Windows<br>
python -m venv .venv<br>
.venv\Scripts\activate<br>

 macOS/Linux<br>
python3 -m venv .venv<br>
source .venv/bin/activate<br>

### Step 3: Install Python Dependencies
pip install -r requirements.txt<br>

### **Step 4: Install FFmpeg**
Windows:  Download from https://ffmpeg.org/download.html --> Add to system PATH<br>
macOS: brew install ffmpeg<br>
Linux: sudo apt-get install ffmpeg<br>

### Step 5: Configure Google Gemini API
GOOGLE_API_KEY=your_api_key_here<br>

### Step 6: Verify Installation
 Test rPPG engine<br>
python src/rppg_engine.py<br><br>

 Test lip-sync engine<br>
python src/lip_sync_engine.py videos/novak_interview_real.mp4<br><br>

 Test news fetcher<br>
python test_news_fetch.py

##  Usage & Running Modes
### Mode 1: Interactive Analysis (Recommended)
Analyze videos with full forensic pipeline:<br>
  python src/gemini_intelligence.py --interactive<br><br>

Interactive Prompt: Example<br>
  Enter video file path (or press Enter for demo clips): videos/novak_interview_real.mp4<br>
  Video type:<br>
   1. Interview/Close-up (enables rPPG + Lip-Sync)<br>
   2. Sports/Wide-shot (skips rPPG + Lip-Sync)<br>
   Choose (1 or 2, default=2): 1<br><br>

  Context: Novak Djokovic post match conference<br>

Output: INFO REAL MODE ENABLED - Will analyze actual video files<br>
INFO Video: videos/novak_interview_real.mp4<br>
INFO Initializing GenAI Client with Stable API (v1)...<br>
INFO Loaded 5 entries from vision report<br>
INFO Transcribing first 15s of novak_interview_real.mp4...<br>
INFO [REAL] Whisper transcript: "I don't know what I can say to them..."<br>
INFO Running Semantic Triangulation...<br>
INFO PULSE DETECTED: Physiological pulse at 71 BPM<br>
INFO Verdict: AUTHENTIC (Confidence: 93%)<br>
INFO Analysis Complete! Saved to gemini_intelligence_report.json<br><br>

### Mode 2: Piracy Simulation
Simulate leak detection and trace source:<br>
  python src/simulate_leak_trace.py<br><br>

Output:<br>
INFO Starting GuardianStream Piracy Detection & Trace Demo<br>
INFO Phase 1: Distributing Content with Invisible Watermarks...<br>
INFO Successfully embedded ID 'PARTNER_A_NETFLIX' into wm_match_ep1.png<br>
INFO Successfully embedded ID 'PARTNER_B_PRIME' into wm_match_ep2.png<br>
INFO Successfully embedded ID 'PARTNER_C_HOTSTAR' into wm_match_ep3.png<br>
INFO PHASE 2: ALERT! Pirated Content Detected on Telegram!<br>
INFO Found suspicious file: TELEGRAM_LEAK_wm_match_ep2.png<br>
INFO Initiating Forensic Analysis...<br>
INFO Extracted ID: 'PARTNER_B_PRIME' from TELEGRAM_LEAK...<br>
Extraction Result: 'PARTNER_B_PRIME'<br>

*==================== LEAK TRACE COMPLETE ====================
Leaked File     : TELEGRAM_LEAK_wm_match_ep2.png
Source ID       : PARTNER_B_PRIME
Verdict         : IDENTIFIED
Action          : ISSUE DMCA & TERMINATE CONTRACT
Report Saved    : leak_trace_report.json
==============================================================*

### Mode 3: Individual Engine Testing
Test specific forensic engines:<br>
 Test rPPG engine<br>
  python src/rppg_engine.py videos/novak_interview_real.mp4<br><br>

 Test lip-sync engine<br>
  python src/lip_sync_engine.py videos/novak_interview_real.mp4 150<br><br>

 Test vision forensics<br>
  python src/vision_forensics.py videos/novak_interview_real.mp4<br><br>

 Test news fetcher<br>
  python test_news_fetch.py "Novak Djokovic Australian Open"<br><br>

 Test semantic dissonance<br>
  python test_dissonance_standalone.py<br>
 


## ** Tech Stack**

### **Backend (Python 3.11+)**
<img width="421" height="271" alt="image" src="https://github.com/user-attachments/assets/faf1cda1-cf9d-4b71-98dd-65cd192289c8" />

### **Frontend**
HTML/CSS/JS(Static Pages)<br>
Next.js, TyspeScript, Tailwind CSS (Future Scope)<br>

## Reports Generated
GuardianStream generates comprehensive forensic reports for legal and analytical use.

### 1. Gemini Intelligence Report (gemini_intelligence_report.json)
Generated by: src/gemini_intelligence.py<br>
Contents:<br>

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
Generated by: src/simulate_leak_trace.py<br>
Contents:<br>

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
Generated by: src/vision_forensics.py<br>
Contents:<br>

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
Generated by: src/action_engine.py<br>
Contents:<br>

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
Generated by: src/action_engine.py<br>
Description: Visual representation of how leaked content spreads across platforms (Twitter → YouTube → Telegram → Torrent sites).<br>

### 6. Terminal Output Logs
All analysis sessions generate real-time terminal logs showing:<br>
Engine initialization<br>
Frame processing progress<br>
Intermediate results (BPM, correlation, credibility)<br>
Final verdict with confidence<br>

Example: <br>
INFO Starting GuardianStream Analysis...<br>
INFO Video: novak_interview_real.mp4<br>
INFO Context: Novak Djokovic post match conference<br>
INFO Loading Whisper model (small)...<br>
INFO Transcribing first 15s of video...<br>
✅ Transcript: "I don't know what I can say to them..."<br>
INFO Running rPPG Analysis (Close-up detected)...<br>
✅ Extracted 228 frames with faces<br>
✅ PULSE DETECTED: Physiological pulse at 71 BPM<br>
✅ rPPG Result: REAL_PERSON<br>
INFO Running Lip-Sync Analysis...<br>
✅ Lip-Sync Result: AUDIO_VIDEO_MATCH<br>
INFO Verdict: AUTHENTIC (Confidence: 93%)<br>
✅ Analysis Complete! Report saved.





