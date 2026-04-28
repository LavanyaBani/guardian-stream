# test_dissonance_standalone.py
# Run this from: D:\guardian-stream\
# Command: python test_dissonance_standalone.py
print("DEBUG: Script started!")  # Add this as line 1

import re

def check_semantic_dissonance(ocr_text: str, audio_transcript: str, news_summary: str) -> dict:
    """
    Triangulates Visual OCR + Audio Transcript + Live News to detect misinformation.
    Returns a dissonance report.
    """
    report = {
        "dissonance_detected": False,
        "confidence": 0.0,
        "reasoning": [],
        "verdict": "CONSISTENT"
    }
    
    # Convert to lowercase for comparison
    ocr = ocr_text.lower()
    audio = audio_transcript.lower()
    news = news_summary.lower()
    
    # 1. Check for Date/Year Mismatch
    ocr_years = re.findall(r'\b(19|20)\d{2}\b', ocr)
    audio_years = re.findall(r'\b(19|20)\d{2}\b', audio)
    
    if ocr_years and audio_years and ocr_years[0] != audio_years[0]:
        report["dissonance_detected"] = True
        report["confidence"] = 0.95
        report["reasoning"].append(f"Year mismatch: Video shows {ocr_years[0]}, Audio claims {audio_years[0]}")
    
    # 2. Check if Audio Claim Contradicts News
    if audio and news:
        contradiction_keywords = ["retiring", "banned", "injured", "scandal", "fake"]
        if any(kw in audio for kw in contradiction_keywords) and "no record" in news:
            report["dissonance_detected"] = True
            report["confidence"] = 0.90
            report["reasoning"].append("Audio makes serious claim not supported by live news")
    
    # 3. Check if OCR and Audio Describe Different Events
    if ocr and audio:
        sports_keywords = ["cricket", "football", "basketball", "match", "game", "goal", "run", "wicket"]
        if any(kw in ocr for kw in sports_keywords) and any(kw in audio for kw in sports_keywords):
            players_ocr = ["rohit", "kohli", "lebron", "messi", "ronaldo"]
            players_audio = ["rohit", "kohli", "lebron", "messi", "ronaldo"]
            ocr_player = next((p for p in players_ocr if p in ocr), None)
            audio_player = next((p for p in players_audio if p in audio), None)
            if ocr_player and audio_player and ocr_player != audio_player:
                report["dissonance_detected"] = True
                report["confidence"] = 0.85
                report["reasoning"].append(f"Player mismatch: Video shows {ocr_player}, Audio mentions {audio_player}")
    
    # Final verdict
    if report["dissonance_detected"]:
        report["verdict"] = "MISLEADING_CONTEXT"
        report["confidence"] = max(report["confidence"], 0.80)
    
    return report

# --- TEST CASES ---
print("🧪 Testing Semantic Dissonance Function (Standalone)...\n")

# Test 1: Year Mismatch (Should detect dissonance)
print("Test 1: Year Mismatch")
result1 = check_semantic_dissonance(
    ocr_text="IND vs SA 2019 World Cup Final",
    audio_transcript="Today in 2024, Rohit Sharma announces retirement",
    news_summary="No record of retirement found in live news"
)
print(f"  Result: {result1}")
print(f"  ✅ PASS" if result1["dissonance_detected"] else "  ❌ FAIL")
print()

# Test 2: Consistent Content (Should NOT detect dissonance)
print("Test 2: Consistent Content")
result2 = check_semantic_dissonance(
    ocr_text="LeBron James Lakers 2023",
    audio_transcript="Great game tonight for the Lakers",
    news_summary="Lakers win against Warriors, LeBron scores 30"
)
print(f"  Result: {result2}")
print(f"  ✅ PASS" if not result2["dissonance_detected"] else "  ❌ FAIL")
print()

# Test 3: Player Mismatch (Should detect dissonance)
print("Test 3: Player Mismatch")
result3 = check_semantic_dissonance(
    ocr_text="Rohit Sharma century vs Australia",
    audio_transcript="Kohli's amazing performance today",
    news_summary="Rohit Sharma scored a century in today's match"
)
print(f"  Result: {result3}")
print(f"  ✅ PASS" if result3["dissonance_detected"] else "  ❌ FAIL")
print()

print("🎉 All tests complete!")