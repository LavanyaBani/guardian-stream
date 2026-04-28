from src.gemini_intelligence import check_semantic_dissonance

# Test Case 1: Year Mismatch
result = check_semantic_dissonance(
    ocr_text="IND vs SA 2019 World Cup Final",
    audio_transcript="Today in 2024, Rohit Sharma announces retirement",
    news_summary="No record of retirement found in live news"
)
print("Test 1 Result:", result)

# Test Case 2: Consistent
result2 = check_semantic_dissonance(
    ocr_text="LeBron James Lakers 2023",
    audio_transcript="Great game tonight for the Lakers",
    news_summary="Lakers win against Warriors, LeBron scores 30"
)
print("Test 2 Result:", result2)