from django.apps import AppConfig


class ProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Production'
    verbose_name = 'প্রোডাকশন | Production '  # Change this to your desired new app name