from book_links_extractor import extract_book_links
from book_parser import parse_page
from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/category/publitsystyka-ta-dokumentalistyka/"


def parse_catalog(url: str):
    soup = fetch_page(url)
    book_links = extract_book_links(soup)
    for book_url in book_links:
        info = parse_page(book_url)
        print(info)


if __name__ == "__main__":
    parse_catalog(TEST_URL)
