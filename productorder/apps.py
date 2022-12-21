from django.apps import AppConfig


class ProductorderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "productorder"

    def ready(self):
        import productorder.signals
