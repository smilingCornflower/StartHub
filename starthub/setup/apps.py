from django.apps import AppConfig


class SetupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "setup"

    already_run = False

    def ready(self) -> None:
        if self.__class__.already_run is False:

            import setup.signals  # noqa: F401
            from setup.setup_event_handlers import setup_event_handlers

            setup_event_handlers()

            self.__class__.already_run = True
