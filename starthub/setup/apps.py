from django.apps import AppConfig


class SetupConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "setup"

    already_run = False

    def ready(self) -> None:
        if self.__class__.already_run is False:
            import setup.signals  # noqa: F401

            self.__class__.already_run = True
