# Guardian Stream

Basic project scaffold.

## Setup

1. Create a virtual environment (example):
   - `python -m venv .venv`
2. Activate it:
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies:
   - `pip install -r requirements.txt`

## Structure

- `src/` - application source code

# 🛡️ GuardianStream: Digital Asset Protection Engine

## 🚀 Problem
Sports media faces massive piracy and deepfake misappropriation. Existing tools only detect exact copies, missing modified or AI-generated fakes.

## 💡 Solution
A scalable, AI-driven platform that:
1.  **Detects Piracy:** Uses Perceptual Hashing (pHash) to find cropped/flipped copies instantly.
2.  **Identifies Deepfakes:** Uses Gemini 1.5 Pro + Google Search to verify if events actually happened.
3.  **Traces Leaks:** Simulates dynamic watermarking to identify the source of unauthorized redistribution.
4.  **Automates Takedowns:** Generates DMCA reports and disables monetization automatically.

## ️ Architecture
- **Data Layer:** Google Cloud Storage (Frames & Assets)
- **Analysis Engine:** 
  - Fast Filter: ImageHash (pHash)
  - Forensics: Cloud Vision API (Watermarks/Logos)
  - Intelligence: Gemini 1.5 Pro with Search Grounding (Context Verification)
- **Action Layer:** Automated Reporting & Takedown Bot

## 🛠️ Tech Stack
- Python, OpenCV, ImageHash
- Google Cloud Platform (Vertex AI, Vision API, BigQuery, Storage)
- Streamlit (Dashboard)

## 📊 Demo Results
*(We will fill this in once your script finishes!)*

