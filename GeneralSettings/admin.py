from django.contrib import admin

from .models import Currency, Unit,Company,Department

admin.site.register(Currency)
admin.site.register(Unit)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    # Define the fields to display and edit in the admin panel
    list_display = ('name', 'address')
    fields = ('name', 'logo','address','phone_number','email','website','established_year')
    # Disable the "Add" button in the admin panel
    def has_add_permission(self, request):
        return False
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    # Define the fields to display and edit in the admin panel
    list_display = ('name', 'description')
    fields = ('name', 'description')

