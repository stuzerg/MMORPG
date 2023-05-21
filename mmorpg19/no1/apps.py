from django.apps import AppConfig


class No1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'no1'
    def ready(self):
        from .tasks import send_spam



