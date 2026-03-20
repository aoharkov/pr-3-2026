import csv
import os
from dataclasses import fields

from model.book_info import BookInfo

DEFAULT_FILE = "02-parse-catalog/output/books.csv"


def save_books_to_csv(books: list[BookInfo], file_path: str = DEFAULT_FILE, append: bool = False):
    fieldnames = [f.name for f in fields(BookInfo)]
    mode = "a" if append else "w"
    write_header = not append or not os.path.exists(file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for book in books:
            writer.writerow({"url": book.url, "title": book.title, "details": book.details})
