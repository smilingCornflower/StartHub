from dataclasses import dataclass


@dataclass
class NewsImageDto:
    image_name: str
    image_url: str


@dataclass
class NewsShortDto:
    id: int
    author_id: int
    title: str
    subtitle: str | None
    cover: str | None
    published_at: str


@dataclass
class NewsFullDto(NewsShortDto):
    content: str
    images: list[NewsImageDto]
