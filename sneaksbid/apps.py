from django.apps import AppConfig


class SneaksbidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sneaksbid'

    def ready(self):
        import sneaksbid.signals