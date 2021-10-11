from django.apps import AppConfig


class NoteConfig(AppConfig):
    name = "note"

    def ready(self):
        # app django tarafından yüklendikten sonra signallerin çalışmasını sağlar
        from . import signals  # noqa unimport: skip
