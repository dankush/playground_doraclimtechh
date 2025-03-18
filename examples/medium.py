import requests
from bs4 import BeautifulSoup

# Define headers to mimic a browser request
headers = {'User-Agent': 'Mozilla/5.0'}

# Define the search URL
query = "site:medium.com pytest after:2025-01-01"
url = f"https://www.google.com/search?q={query}&num=20"

# Send the GET request
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Extract titles from the search results
titles = []
for result in soup.find_all('h3'):
    titles.append(result.text)

# Print top 20 titles
for title in titles[:20]:
    print(title)