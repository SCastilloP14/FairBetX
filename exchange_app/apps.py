from django.apps import AppConfig


class ExchangeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exchange_app"

    def ready(self):
        from .api_scheduler import api_updater
        print('STARTING API...')
        api_updater.start()