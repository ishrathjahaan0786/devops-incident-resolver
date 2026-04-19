import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

def search_fix(error_message: str) -> str:
    """Search the web for a fix for the given error message."""
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        response = client.search(
            query=f"how to fix {error_message} in Python backend service",
            search_depth="advanced",
            max_results=3
        )
        
        results = []
        for r in response.get("results", []):
            results.append(f"Source: {r['url']}\nSummary: {r['content']}\n")
        
        return "\n".join(results) if results else "No fix found."
    
    except Exception as e:
        return f"Search failed: {str(e)}"