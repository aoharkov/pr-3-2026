from bs4 import BeautifulSoup

from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/category/publitsystyka-ta-dokumentalistyka/"


def parse_catalog(url: str) -> list:
    soup = fetch_page(url)
    book_links = extract_book_links(soup)
    return book_links


def extract_book_links(soup: BeautifulSoup):
    book_links = list(dict.fromkeys(
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/product/")
    ))
    return book_links


if __name__ == "__main__":
    links = parse_catalog(TEST_URL)
    print(f"Extracted {len(links)} book links from {TEST_URL}:")
    for link in links:
        print(link)