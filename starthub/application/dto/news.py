from dataclasses import dataclass


@dataclass
class NewsDto:
    id: int
    author_id: int
    title: str
    content: str
    image_url: str
