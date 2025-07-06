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
    content: str
    cover: str


@dataclass
class NewsFullDto(NewsShortDto):
    images: list[NewsImageDto]
