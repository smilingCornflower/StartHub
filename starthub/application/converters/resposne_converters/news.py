from application.dto.news import NewsFullDto, NewsImageDto, NewsShortDto
from domain import constants
from domain.models.news import News


def news_to_full_dto(news: News, cover_url: str, news_image_dtos: list[NewsImageDto]) -> NewsFullDto:
    return NewsFullDto(
        id=news.id,
        author_id=news.author_id,
        title=news.title,
        subtitle=news.subtitle,
        content=news.content,
        published_at=news.published_at.strftime(constants.DATETIME_FORMAT),
        cover=cover_url,
        images=news_image_dtos,
    )


def news_to_short_dto(news: News, cover_url: str) -> NewsShortDto:
    return NewsShortDto(
        id=news.id,
        author_id=news.author_id,
        title=news.title,
        subtitle=news.subtitle,
        published_at=news.published_at.strftime(constants.DATETIME_FORMAT),
        cover=cover_url,
    )
