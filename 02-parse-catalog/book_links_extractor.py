from bs4 import BeautifulSoup

from fetcher import fetch_page

TEST_URL = "https://vivat.com.ua/category/it-knyhy/"


def extract_book_links(soup: BeautifulSoup):
    book_links = list(dict.fromkeys(
        f"https://vivat.com.ua{a['href']}"
        for a in soup.find_all("a", href=True)
        if a["href"].startswith("/product/")
    ))
    return book_links


def extract_book_links_from_multiple_pages(base_url: str) -> list[str]:
    all_links = []
    page = 1
    while True:
        url = f"{base_url}?page={page}"
        soup = fetch_page(url)
        links = extract_book_links(soup)
        if not links:
            break
        all_links.extend(links)
        print(f"Extracted {len(links)} links from {url} (total: {len(all_links)})")
        page += 1
    return list(dict.fromkeys(all_links))


if __name__ == "__main__":
    extracted_links = extract_book_links_from_multiple_pages(TEST_URL)
    print(f"Extracted {len(extracted_links)} book links from {TEST_URL}:")
