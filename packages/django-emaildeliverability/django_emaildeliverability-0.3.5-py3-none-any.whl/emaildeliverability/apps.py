from django.apps import AppConfig
from emaildeliverability.settings import check_config


class EmaildeliverabilityConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "emaildeliverability"

    def ready(self):
        check_config()
