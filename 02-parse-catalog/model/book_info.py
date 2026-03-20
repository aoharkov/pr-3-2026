from dataclasses import dataclass


@dataclass
class BookInfo:
    url: str
    title: str
    details: str

    def __str__(self):
        return f"URL: {self.url}\nTitle: {self.title}\nDetails: {self.details[:100]}..."
