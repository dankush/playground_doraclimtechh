import time
import random
from typing import List, Dict
from duckduckgo_search import DDGS
from random import uniform
import logging


def simple_duckduckgo_search(query: str, max_results: int = 5):
    """Perform a simple DuckDuckGo search and print the results."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['href']}")
            print(f"   Snippet: {result['body']}")

if __name__ == "__main__":
    search_query = "QA automation best practices 2025"
    print(f"Searching for: {search_query}\n")
    simple_duckduckgo_search(search_query)

exit()
# # Setup logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# # Global delay settings and maximum retry attempts
# BASE_DELAY = 5
# MAX_RETRIES = 3

# # List of user-agents for rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# ]

# # List of proxies for rotation (if available; leave empty if not)
# PROXIES = [
#     # Example proxies:
#     # "http://proxy1.example.com:8080",
#     # "http://proxy2.example.com:8080",
# ]

# # Simple in-memory cache for query results
# CACHE = {}

# # Define target QA resources
# QA_RESOURCES = [
#     "testguild.com/blog",
#     "softwaretestingmagazine.com",
#     "techtarget.com/searchsoftwarequality",
#     "testing.googleblog.com",
#     "saucelabs.com/blog",
#     "medium.com",
#     "ministryoftesting.com",
#     "qamadness.com",
# ]

# def get_random_user_agent() -> str:
#     """Select a random user-agent string."""
#     return random.choice(USER_AGENTS)

# def get_random_proxy() -> Dict[str, str]:
#     """Select a random proxy if available."""
#     if PROXIES:
#         proxy = random.choice(PROXIES)
#         return {"http": proxy, "https": proxy}
#     return None

# def exponential_backoff_delay(attempt: int) -> float:
#     """
#     Calculate an exponential backoff delay with jitter.
#     Delay = BASE_DELAY * (2^attempt) + random jitter.
#     """
#     jitter = uniform(0, 1)
#     return BASE_DELAY * (2 ** attempt) + jitter

# def search_qa_articles(query: str, max_results: int = 3) -> List[Dict[str, str]]:
#     """
#     Search for recent QA articles with AI initiatives from specified resources.
    
#     Args:
#         query (str): The search query (e.g., "QA with AI initiatives 2025").
#         max_results (int): Maximum number of results per resource.
    
#     Returns:
#         List[Dict[str, str]]: A list of results with title, URL, and snippet.
#     """
#     results = []
#     with DDGS() as ddgs:
#         for site in QA_RESOURCES:
#             cache_key = f"{site}:{query}:{max_results}"
#             if cache_key in CACHE:
#                 logging.info(f"Cache hit for {site}")
#                 site_results = CACHE[cache_key]
#             else:
#                 retries = 0
#                 site_results = []
#                 while retries < MAX_RETRIES:
#                     # Add delay between requests with small random variation
#                     time.sleep(BASE_DELAY + uniform(0, 0.5))
                    
#                     # Randomize user-agent and proxy for each attempt
#                     user_agent = get_random_user_agent()
#                     proxy = get_random_proxy()
                    
#                     # Note: duckduckgo_search library may not expose header/proxy parameters;
#                     # these values are included to illustrate best practices.
                    
#                     # Construct site-specific query with a time filter
#                     search_query = f"{query} site:{site} -inurl:(signup login)"
#                     try:
#                         logging.info(f"Searching {site} with query: {search_query}")
#                         # Fetch results, using 'timelimit' for recent (last week) content
#                         site_results = list(ddgs.text(search_query, max_results=max_results, timelimit="w"))
#                         CACHE[cache_key] = site_results  # Cache the successful results
#                         break  # Exit loop on successful search
#                     except Exception as e:
#                         error_str = str(e)
#                         if "202" in error_str or "Ratelimit" in error_str:
#                             wait_time = exponential_backoff_delay(retries)
#                             logging.warning(f"Rate limit encountered for {site}. "
#                                             f"Retrying in {wait_time:.2f} seconds... (Attempt {retries + 1})")
#                             time.sleep(wait_time)
#                         else:
#                             logging.error(f"Error searching {site}: {e}")
#                             break
#                         retries += 1
#                 if not site_results:
#                     logging.error(f"No results for {site} after {MAX_RETRIES} retries.")
#             if site_results:
#                 for result in site_results:
#                     results.append({
#                         "title": result.get("title", "No Title"),
#                         "url": result.get("href", "No URL"),
#                         "snippet": result.get("body", "No Snippet")
#                     })
#     return results

# def display_results(results: List[Dict[str, str]]) -> None:
#     """Display search results in a user-friendly format."""
#     if not results:
#         print("No results found within the last week.")
#         return
    
#     print("\n=== Latest QA Articles with AI Initiatives (Last Week) ===")
#     for i, result in enumerate(results, 1):
#         print(f"\n{i}. {result['title']}")
#         print(f"   URL: {result['url']}")
#         print(f"   Snippet: {result['snippet'][:150]}...")

# def main():
#     """Main function to run the search."""
#     query = "QA with AI initiatives 2025"
#     print(f"Searching for: {query} (published in the last week)")
#     results = search_qa_articles(query, max_results=3)
#     display_results(results)

# if __name__ == "__main__":
#     try:
#         main()
#     except ImportError as e:
#         print(f"Missing dependency: {e}. Please install 'duckduckgo-search' via pip.")
#     except Exception as e:
#         print(f"An error occurred: {e}")