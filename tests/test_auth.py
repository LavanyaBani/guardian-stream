# Quick sanity check to verify Google Cloud credentials are working.
# Run this if you get permission errors in the main app.
import os
from google.cloud import storage

# If you didn't use Option B above, uncomment the next line:
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account-key.json"

def test_connection():
    try:
        # Try to list buckets (requires Storage Admin role)
        client = storage.Client()
        buckets = client.list_buckets()
        print("✅ Success! Connected to Google Cloud.")
        print(f"Found {len(list(buckets))} buckets.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()