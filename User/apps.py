from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User'
    verbose_name = 'Kullanıcı İşlemleri'

    def ready(self):
        import User.signals
