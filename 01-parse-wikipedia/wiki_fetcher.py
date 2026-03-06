from urllib.parse import unquote

import requests

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
BASE_URL = "https://en.wikipedia.org"

HEADERS = {
    "User-Agent": (
        "DemoWikiBot/1.0 "
        "(https://github.com/your-repo; your-email@example.com) "
        "python-requests/" + requests.__version__
    ),
    "Accept": "text/html",
    "Accept-Language": "en",
}


def fetch_page(url: str) -> dict:
    """Fetch a Wikipedia page and return its title, URL, and HTML."""
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    title = unquote(response.url.split("/wiki/")[-1]).replace("_", " ")
    return {"title": title, "url": response.url, "html": response.text}


def get_random_wikipedia_page() -> dict:
    """Fetch a random Wikipedia page."""
    return fetch_page(RANDOM_URL)
