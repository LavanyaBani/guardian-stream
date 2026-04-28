import logging
import feedparser
import urllib.parse
import re

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Trusted sports/news sources for credibility scoring (when news IS found)
TRUSTED_SOURCES = [
    "espn", "bbc", "icc", "nba", "reuters", "ap", 
    "cricbuzz", "wion", "espn.in", "sky sports", 
    "the athletic", "sportskeeda", "ndtv sports"
]

def fetch_live_news(query: str, num_results: int = 3, trusted_only: bool = True) -> list:
    """
    Fetches live news articles via Google News RSS.
    
    Returns empty list if fetch fails — other forensic layers handle the verdict.
    
    Args:
        query: Search query
        num_results: Number of results to return
        trusted_only: If True, prioritize verified sources
    
    Returns:
        List of article dicts with title, snippet, source, url, trusted
        Returns [] if fetch fails (no fallback simulation)
    """
    results = []
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        logger.info(f" Fetching RSS feed for: '{query}'")
        feed = feedparser.parse(rss_url)
        
        for entry in feed.entries[:15]:  # Scan more to find trusted sources
            # Handle source safely (can be dict, object, or None)
            source_obj = entry.get("source")
            if source_obj is None:
                source = ""
            elif isinstance(source_obj, dict):
                source = source_obj.get("title", "").lower()
            elif hasattr(source_obj, 'text'):
                source = source_obj.text.lower()
            else:
                source = str(source_obj).lower()
            
            title = entry.get("title", "")
            
            # Handle snippet safely
            snippet_obj = entry.get("summary") or entry.get("description") or ""
            if isinstance(snippet_obj, dict):
                snippet = snippet_obj.get("value", "")
            elif hasattr(snippet_obj, 'text'):
                snippet = snippet_obj.text
            else:
                snippet = str(snippet_obj)
            snippet = re.sub(r'<.*?>', '', snippet).strip()
            
            url = entry.get("link", "")
            
            # Check if trusted
            is_trusted = any(ts in source for ts in TRUSTED_SOURCES) if source else False
            
            article = {
                "title": title,
                "snippet": snippet[:200],
                "source": source,
                "url": url,
                "trusted": is_trusted
            }
            
            # Filter by trusted if requested
            if trusted_only and not is_trusted:
                continue
                
            results.append(article)
            
            if len(results) >= num_results:
                break
        
        trusted_count = sum(1 for r in results if r["trusted"])
        logger.info(f" Found {len(results)} articles ({trusted_count} from trusted sources)")
        return results
        
    except Exception as e:
        logger.warning(f" News fetch failed: {e} (other forensic layers will handle verification)")
        return []

def get_news_credibility_summary(results: list) -> dict:
    """Calculate credibility metrics for display."""
    if not results:
        return {"avg_credibility": 0, "trusted_count": 0, "total": 0}
    
    trusted = sum(1 for r in results if r.get("trusted", False))
    total = len(results)
    
    return {
        "avg_credibility": round((trusted / total) * 100) if total > 0 else 0,
        "trusted_count": trusted,
        "total": total,
        "sources": list(set(r["source"] for r in results if r["source"]))
    }

if __name__ == "__main__":
    print(" Testing News Fetcher (No Fallback)\n")
    
    test_queries = ["cricket world cup", "novak djokovic", "hawking deepfake"]
    
    for query in test_queries:
        print(f" Query: '{query}'")
        results = fetch_live_news(query, num_results=2, trusted_only=True)
        if results:
            for r in results:
                badge = "Trusted" if r["trusted"] else "Not-Trusted"
                print(f"  {badge} {r['title'][:50]}... ({r['source']})")
        else:
            print("    No results (API unavailable — other engines will verify)")
        print()
    
    print(" Test complete!")