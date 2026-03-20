from book_links_extractor import extract_book_links
from book_parser import parse_page
from csv_storage import save_books_to_csv
from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/category/publitsystyka-ta-dokumentalistyka/"


def parse_catalog(url: str):
    soup = fetch_page(url)
    book_links = extract_book_links(soup)
    books = [parse_page(book_url) for book_url in book_links]
    save_books_to_csv(books)
    print(f"\nSaved {len(books)} books to CSV")


if __name__ == "__main__":
    parse_catalog(TEST_URL)
