import os
from google import genai

# Get Key from Env
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key or "PASTE" in api_key:
    print("❌ ERROR: API Key not found in environment variable.")
    print("   Run: $env:GOOGLE_API_KEY='AIza...'")
    exit()

print(f"🔑 Testing Key: {api_key[:10]}...")

try:
    # Initialize Client with Stable V1
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    print("🔍 Checking available models...")
    
    # List of models to test
    models_to_test = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    found_model = None
    
    for model_name in models_to_test:
        try:
            # Try to get model info
            model = client.models.get(model=model_name)
            print(f"✅ SUCCESS: Model '{model_name}' is ACCESSIBLE!")
            print(f"   Display Name: {model.display_name}")
            found_model = model_name
            break # Stop at first success
        except Exception as e:
            print(f"⚠️  Failed to access '{model_name}': {str(e)[:60]}...")

    if found_model:
        print("\n🎉 RESULT: Your API Key is WORKING!")
        print(f"   You can now use model: '{found_model}' in your main script.")
        
        # Quick Generation Test
        print("\n🧪 Running quick generation test...")
        response = client.models.generate_content(
            model=found_model,
            contents="Say 'GuardianStream Online' in one sentence."
        )
        print(f"   AI Response: {response.text}")
        
    else:
        print("\n❌ RESULT: No models accessible yet.")
        print("   Possible reasons:")
        print("   1. 'Generative Language API' is not enabled in Google Cloud Console.")
        print("   2. API Key was created for a different project.")
        print("   3. Still waiting for propagation (try again in 1 more hour).")

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")