import requests


# RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
RANDOM_URL = "https://en.wikipedia.org/wiki/Cloudy_with_a_Chance_of_Meatballs_(video_game)"

HEADERS = {
    "User-Agent": "DemoWikiBot/1.0 (https://github.com/your-repo; your-email@example.com) python-requests/" + requests.__version__,
    "Accept": "text/html",
    "Accept-Language": "en",
}


def get_random_wikipedia_page() -> dict:
    """Fetch a random Wikipedia page and return its title, URL, and HTML content."""
    response = requests.get(RANDOM_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    return {
        "title": response.url.split("/wiki/")[-1].replace("_", " "),
        "url": response.url,
        "html": response.text,
    }


if __name__ == "__main__":
    page = get_random_wikipedia_page()
    print(f"Title: {page['title']}")
    print(f"URL:   {page['url']}")
    print(f"HTML length: {len(page['html'])} chars")
