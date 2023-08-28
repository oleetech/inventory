from django.contrib import admin
from .forms import CustomBusinessPartnerForm
from .models import  BusinessPartner
@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'address')
    search_fields = ('name', 'code')
    list_filter = ('currency_type', 'vendor_type')
    ordering = ('name',)
    readonly_fields = ('code',)  
    form = CustomBusinessPartnerForm 
    




