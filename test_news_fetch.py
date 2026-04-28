# test_news_fetch.py
import feedparser
import urllib.parse

query = "cricket world cup"
encoded = urllib.parse.quote(query)
rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"

print(f"🔍 Testing RSS URL: {rss_url}\n")

try:
    feed = feedparser.parse(rss_url)
    print(f"✅ Feed parsed successfully")
    print(f"📊 Total entries in feed: {len(feed.entries)}")
    
    if feed.entries:
        print(f"\n📰 First 3 entries:")
        for i, entry in enumerate(feed.entries[:3], 1):
            title = entry.get("title", "No title")
            source = entry.get("source", "Unknown")
            print(f"  {i}. {title[:70]}... [Source: {source}]")
    else:
        print(f"\n⚠️  Feed returned 0 entries")
        print(f"   Possible causes:")
        print(f"   • Google RSS rate limiting")
        print(f"   • Geo-blocking (your IP region)")
        print(f"   • Query encoding issue")
        print(f"   • Temporary Google service issue")
        
except Exception as e:
    print(f"❌ Error: {e}")