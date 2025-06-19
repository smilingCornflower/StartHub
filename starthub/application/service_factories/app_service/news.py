from application.ports.app_service_factory import AbstractAppServiceFactory
from application.service_factories.domain_service.news import NewsServiceFactory
from application.services.news import NewsAppService


class NewsAppServiceFactory(AbstractAppServiceFactory[NewsAppService]):
    @staticmethod
    def create_service() -> NewsAppService:
        return NewsAppService(
            news_service=NewsServiceFactory.create_service(),
        )
