from bs4 import BeautifulSoup

from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/product/dykyi-zakhid-skhidnoi-yevropy/#details"


def parse_page(url: str) -> dict:
    soup = fetch_page(url)
    title = get_title_from_html(soup)
    details = get_details_from_html(soup)
    return {"url": url, "title": title, "details": details}


def get_title_from_html(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    return get_text_from_element(h1)


def get_details_from_html(soup: BeautifulSoup) -> str:
    panel = soup.find(id="detailsPanel")
    return get_text_from_element(panel)


def get_text_from_element(element) -> str:
    return element.get_text(strip=True) if element else ""


def print_parsed_data(parsed_data: dict):
    print(f"URL: {parsed_data['url']}")
    print(f"Title: {parsed_data['title']}")
    print(f"Details: {parsed_data['details']}")


if __name__ == "__main__":
    parsed_data = parse_page(TEST_URL)
    print_parsed_data(parsed_data)
