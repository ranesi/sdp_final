from django.apps import AppConfig


class TaWebConfig(AppConfig):
    name = 'ta_web'

    def ready(self):
        import ta_web.signals