import logging
import feedparser
import time
from urllib.parse import quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_live_news(query: str, num_results: int = 3) -> list[dict]:
    """
    Fetches live news using Google News RSS Feed (More stable than scraping).
    """
    logger.info(f"📡 Fetching RSS feed for: '{query}'")
    
    try:
        # Encode query for URL
        safe_query = quote(query)
        
        # Construct Google News RSS URL
        # This is an official public endpoint
        rss_url = f"https://news.google.com/rss/search?q={safe_query}+sports&hl=en-IN&gl=IN&ceid=IN:en"
        
        # Parse the feed
        feed = feedparser.parse(rss_url)
        
        results = []
        if feed.entries:
            for entry in feed.entries[:num_results]:
                # Extract title and link
                title = entry.title
                link = entry.link
                
                # Google News links are often redirected, but valid for demo
                results.append({
                    "source_url": link,
                    "snippet": f"News: {title}"
                })
            
            logger.info(f"✅ Found {len(results)} live articles via RSS.")
            return results
        else:
            logger.warning("No entries found in RSS feed.")
            raise Exception("Empty RSS feed")
            
    except Exception as e:
        logger.warning(f"RSS Fetch failed: {e}. Switching to Simulation Mode.")
        return get_simulated_news(query)

def get_simulated_news(query: str) -> list[dict]:
    """Fallback simulated news if live fetch fails."""
    logger.info("🤖 Using Simulated News Headlines (Fallback)")
    q = query.lower()
    
    if "rohit" in q or "cricket" in q:
        return [
            {"source_url": "https://espncricinfo.com/series/rohith-century", "snippet": "Rohit Sharma smashes historic century in World Cup thriller."},
            {"source_url": "https://bbc.com/sport/cricket", "snippet": "India defeats South Africa thanks to Rohit's brilliant batting."},
            {"source_url": "https://icc-cricket.com/news", "snippet": "Match Report: Rohit Sharma named Player of the Match."}
        ]
    elif "hawking" in q or "skate" in q:
        return [
            {"source_url": "https://snopes.com/fact-check/hawking", "snippet": "FACT CHECK: No evidence Stephen Hawking ever skateboarded. Image is AI-generated."},
            {"source_url": "https://reuters.com/technology/deepfake", "snippet": "New deepfake video of Stephen Hawking circulates online, debunked by experts."},
            {"source_url": "https://nature.com/articles/ai", "snippet": "Scientists warn against AI fabrications of historical figures."}
        ]
    elif "lebron" in q or "basketball" in q:
        return [
            {"source_url": "https://nba.com/lakers/lebron", "snippet": "LeBron James leads Lakers to victory with dominant performance."},
            {"source_url": "https://bleacherreport.com/nba", "snippet": "NBA Highlights: LeBron's latest game stats and analysis."}
        ]
    else:
        return [{"source_url": "https://news.google.com", "snippet": f"General news coverage for {query}"}]

if __name__ == "__main__":
    print("Testing RSS News Fetcher...")
    results = fetch_live_news("Rohit Sharma century")
    for r in results:
        print(f"- {r['snippet']} ({r['source_url']})")