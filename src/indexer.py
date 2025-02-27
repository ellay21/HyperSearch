import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

# Defining the schema for indexing
schema = Schema(title=ID(stored=True), content=TEXT(stored=True))

# Creating index directory if it doesn't exist
if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)

def crawl_and_index(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string.strip() if soup.title else "No Title"
    text = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])[:5000]  # Limit text to 5000 chars

    # Create writer inside function to avoid conflicts
    writer = ix.writer()
    writer.add_document(title=title, content=text)
    writer.commit()

    print(f"Indexed: {title}")

urls = ["https://en.wikipedia.org/wiki/Bitwise_operation#OR"]
for url in urls:
    crawl_and_index(url)
