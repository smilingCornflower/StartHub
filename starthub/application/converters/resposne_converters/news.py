from domain.models.news import News
from application.dto.news import NewsDto


def news_to_dto(news: News):
    return NewsDto(
        id=news.id, author_id=news.author_id, title=news.title, content=news.content, image_url=news.image,
    )

