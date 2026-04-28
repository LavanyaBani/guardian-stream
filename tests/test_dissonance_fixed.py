import re

def check_semantic_dissonance(ocr_text: str, audio_transcript: str, news_summary: str) -> dict:
    report = {
        "dissonance_detected": False,
        "confidence": 0.0,
        "reasoning": [],
        "verdict": "CONSISTENT"
    }
    
    ocr = ocr_text.lower()
    audio = audio_transcript.lower()
    news = news_summary.lower()
    
    # FIXED REGEX
    ocr_years = re.findall(r'\b(19\d{2}|20\d{2})\b', ocr)
    audio_years = re.findall(r'\b(19\d{2}|20\d{2})\b', audio)
    
    print(f"  OCR Years: {ocr_years}")
    print(f"  Audio Years: {audio_years}")
    
    if ocr_years and audio_years and ocr_years[0] != audio_years[0]:
        report["dissonance_detected"] = True
        report["confidence"] = 0.95
        report["reasoning"].append(f"Year mismatch: Video shows {ocr_years[0]}, Audio claims {audio_years[0]}")
    
    if audio and news:
        contradiction_keywords = ["retiring", "retirement", "banned", "injured", "scandal", "fake"]
        if any(kw in audio for kw in contradiction_keywords) and ("no record" in news or "not found" in news):
            report["dissonance_detected"] = True
            report["confidence"] = 0.90
            report["reasoning"].append("Audio claim not supported by news")
    
    if report["dissonance_detected"]:
        report["verdict"] = "MISLEADING_CONTEXT"
    
    return report

print(" Testing FIXED Semantic Dissonance...\n")

# Test 1: Year Mismatch
print("Test 1: Year Mismatch (2019 vs 2024)")
r1 = check_semantic_dissonance(
    "IND vs SA 2019 World Cup",
    "Today in 2024, Rohit announces retirement",
    "No record of retirement found"
)
print(f"  Result: {r1}")
print(f"  {'✅ PASS' if r1['dissonance_detected'] else '❌ FAIL'}\n")

# Test 2: Consistent
print("Test 2: Consistent Content")
r2 = check_semantic_dissonance(
    "LeBron Lakers 2023",
    "Great game for Lakers",
    "Lakers win, LeBron scores 30"
)
print(f"  Result: {r2}")
print(f"  {'✅ PASS' if not r2['dissonance_detected'] else '❌ FAIL'}\n")

print("Tests Complete!")