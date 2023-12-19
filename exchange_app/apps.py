from django.apps import AppConfig


class ExchangeAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "exchange_app"

    def ready(self):
        from .api_scheduler.api_updater import start
        print('STARTING API...')
        start()