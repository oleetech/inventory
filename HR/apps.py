from django.apps import AppConfig


class HrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HR'
    verbose_name = 'Human Resources  '
    def ready(self):
        import HR.signals    