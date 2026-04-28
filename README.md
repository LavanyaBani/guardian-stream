# 🛡️ GuardianStream - AI-Powered Sports Media Protection

## 🏆 Hackathon Project
**Multi-layer forensic engine for detecting piracy, deepfakes, and content misappropriation in sports media.**

---

## 🚀 Features

### 1. **Piracy Detection**
- Perceptual hashing (pHash) for modified content detection
- Detects cropped, flipped, and re-encoded copies

### 2. **Deepfake Verification**
- Live news intelligence via RSS feeds
- Cross-modal semantic dissonance detection
- OCR-based context verification

### 3. **Forensic Watermarking**
- LSB steganography for leak tracing
- Identifies specific distributor who leaked content

### 4. **Propagation Tracking**
- Visual graph showing content spread across platforms
- Automated DMCA report generation

### 5. **Decision Engine**
- Multi-layer confidence scoring
- Resilience mode (works offline if API fails)

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Computer Vision:** OpenCV, PIL
- **AI/ML:** Google Gemini, Vertex AI, Whisper
- **Cloud:** Google Cloud Storage, Vision API
- **Forensics:** Stegano (LSB), ImageHash
- **Visualization:** NetworkX, Matplotlib

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/guardian-stream.git
cd guardian-stream

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_API_KEY="your-api-key"

