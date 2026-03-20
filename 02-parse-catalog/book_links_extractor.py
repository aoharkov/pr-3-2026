from bs4 import BeautifulSoup

from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/category/publitsystyka-ta-dokumentalistyka/"


def extract_book_links(soup: BeautifulSoup):
    book_links = list(dict.fromkeys(
        f"https://vivat.com.ua{a['href']}"
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/product/")
    ))
    return book_links


if __name__ == "__main__":
    soup = fetch_page(TEST_URL)
    links = extract_book_links(soup)
    print(f"Extracted {len(links)} book links from {TEST_URL}:")
    for link in links:
        print(link)