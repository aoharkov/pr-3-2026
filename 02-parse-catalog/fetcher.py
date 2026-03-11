import requests

TEST_URL = "https://vivat.com.ua/product/dykyi-zakhid-skhidnoi-yevropy/#details"

HEADERS = {
    "User-Agent": (
        "DemoWikiBot/1.0 "
        "(https://github.com/your-repo; your-email@example.com) "
        "python-requests/" + requests.__version__
    ),
    "Accept": "text/html",
    "Accept-Language": "en",
}


def fetch_page(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    html_content = fetch_page(TEST_URL)
    print(f"Fetched HTML content from {TEST_URL} (length: {len(html_content)} characters)")
