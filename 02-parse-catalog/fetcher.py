from time import sleep

import requests
from bs4 import BeautifulSoup

TEST_URL = "https://vivat.com.ua/product/dykyi-zakhid-skhidnoi-yevropy/#details"
REQUEST_DELAY = 0.1

HEADERS = {
    "User-Agent": (
        "DemoWikiBot/1.0 "
        "(https://github.com/your-repo; your-email@example.com) "
        "python-requests/" + requests.__version__
    ),
    "Accept": "text/html",
    "Accept-Language": "en",
}


def fetch_page(url: str) -> BeautifulSoup:
    sleep(REQUEST_DELAY)
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


if __name__ == "__main__":
    soup = fetch_page(TEST_URL)
    print(f"Fetched HTML content from {TEST_URL} (length: {len(soup.prettify())} characters)")
