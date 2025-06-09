from application.service_factories.user import UserServiceFactory


class Gateway:
    user_app_service = UserServiceFactory.create_service()
