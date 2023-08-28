from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import SalesOrderInfo, SalesOrderItem
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item

class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  # Replace 'name' with the appropriate field

class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = '__all__'
        widgets = {
            'ItemName': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        }

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    form = SalesOrderItemForm
    extra = 1

class SalesOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesOrderInfo
        fields = '__all__'
        widgets = {
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'CustomerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }

class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]
    
    def save_model(self, request, obj, form, change):
        if obj.CustomerName:
            obj.Address = obj.CustomerName.address
        super().save_model(request, obj, form, change)
        
    class Media:
        js = ('js/salesorder.js',)
        defer = True

admin.site.register(SalesOrderInfo, SalesOrderInfoAdmin)
