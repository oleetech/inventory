from django.apps import AppConfig


class ItemmasterdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ItemMasterData'
    verbose_name = 'Inventory  '  # Change this to your desired new app name
    def ready(self):
        import ItemMasterData.signals