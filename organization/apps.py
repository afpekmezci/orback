from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'organization'
    def ready(self):
        # app django tarafından yüklendikten sonra signallerin çalışmasını sağlar
        from . import signals  # noqa unimport: skip
