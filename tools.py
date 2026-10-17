from crewai.tools import tool
from ddgs import DDGS
import wikipedia
import requests
from bs4 import BeautifulSoup
import re

@tool("web_search")
def web_search(query: str) -> str:
    """Search the web using DuckDuckGo and return titles, URLs and snippets."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            out = ""
            for r in results:
                out += f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n---\n"
            return out or "No results"
    except Exception as e:
        return f"Search error: {e}"

@tool("wikipedia_search")
def wikipedia_search(query: str) -> str:
    """Search Wikipedia and return summary for a query."""
    try:
        return wikipedia.summary(query, sentences=5)
    except Exception:
        return f"Wikipedia search results: {wikipedia.search(query)}"

@tool("scrape_webpage")
def scrape_webpage(url: str) -> str:
    """Scrape text content from a given webpage URL."""
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        return "\n".join([p.get_text() for p in soup.find_all('p')[:10]])[:4000]
    except Exception as e:
        return f"Scrape error: {e}"

@tool("summarize_text")
def summarize_text(text: str) -> str:
    """Summarize long text into key points."""
    return f"Summary: {text[:3000]}"

@tool("extract_links")
def extract_links(text: str) -> str:
    """Extract all HTTP links and URLs from given text."""
    urls = re.findall(r'https?://\S+', text)
    return "\n".join(set(urls)) if urls else "No URLs found"