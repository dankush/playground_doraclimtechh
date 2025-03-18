import time
import random
import requests
from typing import List, Dict
from duckduckgo_search import DDGS
import logging
import warnings
import sys
from urllib3.exceptions import NotOpenSSLWarning

warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

sys.path.append('.')
from config import TELEGRAM_TOPIC_CONFIGS, ChatTopic
qa_ai_config = TELEGRAM_TOPIC_CONFIGS[ChatTopic.QA_WITH_AI]
TELEGRAM_BOT_TOKEN = qa_ai_config.token
TELEGRAM_CHAT_ID = qa_ai_config.chat_id


def send_telegram_message(message: str):
    """Send a message to the Telegram group."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        logging.info("Message sent to Telegram successfully.")
    else:
        logging.error(f"Failed to send message: {response.text}")


def duckduckgo_search_with_retries(query: str, max_results: int = 10, days_ago: int = 7, retries: int = 3, use_domain_filter: bool = False) -> List[Dict[str, str]]:
    """
    Perform a DuckDuckGo search with retry logic to handle rate limits.
    """
    results = []
    attempts = 0
    backoff = 2  # Start with 2-second wait time
    
    while attempts < retries:
        try:
            with DDGS() as ddgs:
                time_filter = "w" if days_ago == 7 else "d" if days_ago == 1 else "m" if days_ago == 30 else "w"
                search_query = query
                
                if use_domain_filter:
                    allowed_domains = [
                        "testguild.com", "softwaretestingmagazine.com", "techtarget.com",
                        "testing.googleblog.com", "saucelabs.com", "medium.com",
                        "ministryoftesting.com", "qamadness.com", "googl.com"
                    ]
                    search_query = f"site:({' OR site:'.join(allowed_domains)}) {search_query}"
                search_results = list(ddgs.text(
                    search_query,
                    max_results=max_results,
                    timelimit=time_filter
                ))
                for result in search_results:
                    date = result.get("datePublished", result.get("date", "No Date"))
                    results.append({
                        "title": result.get("title", "No Title"),
                        "url": result.get("href", "No URL"),
                        "snippet": result.get("body", "No Snippet"),
                        "date": date
                    })
                
                return results
        except Exception as e:
            logging.warning(f"Search attempt {attempts + 1} failed: {str(e)}")
            attempts += 1
            time.sleep(backoff)
            backoff *= 2  # Exponential backoff
    
    logging.error("DuckDuckGo search failed after retries.")
    return results


def format_results_for_telegram(results: List[Dict[str, str]]) -> str:
    """Format the search results into a message suitable for Telegram."""
    if not results:
        return "No relevant articles found for your query."
    
    message = "🔍 *QA & AI Articles* 🔍\n\n"
    MAX_SNIPPET_LENGTH = 200
    MAX_RESULTS = 10
    
    for i, result in enumerate(results[:MAX_RESULTS], 1):
        message += f"*{i}. {result['title'][:100]}*\n"
        # message += f"📅 {result['date']}\n"
        message += f"📌 [Read more]({result['url']})\n"
        message += f"📝 {result['snippet'][:MAX_SNIPPET_LENGTH]}...\n\n"
    
    if len(message) > 4000:
        return message[:3900] + "\n\n... (truncated)"
    
    return message


def main():
    """Main function to run the search and send results to Telegram."""
    query = "QA with AI tips, solutions and examples 2025" # Define your search query here
    logging.info(f"Searching for: {query}")
    
    results = duckduckgo_search_with_retries(query, max_results=10)
    formatted_message = format_results_for_telegram(results)
    
    send_telegram_message(formatted_message)


if __name__ == "__main__":
    main()