from django.apps import AppConfig


class ProductionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Production'
    verbose_name = 'Production '  # Change this to your desired new app name
    app_icon = 'fas fa-cogs'  # Specify the icon for your app (Font Awesome icon class)
    