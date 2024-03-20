from django.apps import AppConfig


class WallConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wall'

    def ready(self):
        pass
#        from . import signals  # выполнение модуля -> регистрация сигналов
