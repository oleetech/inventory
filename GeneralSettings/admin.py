from django.contrib import admin

from .models import Currency, Unit,Company

admin.site.register(Currency)
admin.site.register(Unit)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Define the fields to display and edit in the admin panel
    list_display = ('name', 'address')
    fields = ('name', 'address')
    # Disable the "Add" button in the admin panel
    def has_add_permission(self, request):
        return False
