from django.apps import AppConfig


class TextsConfig(AppConfig):
    name = 'texts'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import signals
