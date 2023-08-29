from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import SalesOrderInfo, SalesOrderItem 
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item

class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  

class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = '__all__'
        widgets = {
            'ItemName': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains'])
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
            'OrderNumber': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'CustomerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = SalesOrderInfo.objects.order_by('-OrderNumber').first()
            if last_order:
                next_order_number = last_order.OrderNumber + 1
            else:
                next_order_number = 1

            self.initial['OrderNumber'] = next_order_number
            
                    
@admin.register(SalesOrderInfo)
class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]
    

        
    class Media:
        js = ('js/salesorder.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.Address:
            if obj.CustomerName :
                obj.Address = obj.CustomerName.address
        super().save_model(request, obj, form, change)
'''
  ____           _   _                               
 |  _ \    ___  | | (_) __   __   ___   _ __   _   _ 
 | | | |  / _ \ | | | | \ \ / /  / _ \ | '__| | | | |
 | |_| | |  __/ | | | |  \ V /  |  __/ | |    | |_| |
 |____/   \___| |_| |_|   \_/    \___| |_|     \__, |
                                               |___/ 
'''

from .models import DeliveryInfo,DeliveryItem
class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['DocNo','SalesOrder','CustomerName','Address','TotalAmount','TotalQty']
        widgets = {
            'DocNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'CustomerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['ItemName','Quantity','Price','PriceTotal']
        widgets = {

            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'ItemName': DeliveryItemModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        }
class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1  
    form = DeliveryItemForm
    
    
@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('DocNo',  'TotalQty','TotalAmount')
    inlines = [DeliveryItemInline] 
    form = DeliveryInfoForm
  
  
        
    class Media:
        js = ('js/delivery.js',)
        defer = True         
        
     
    def save_model(self, request, obj, form, change):
        if not obj.Address:
            if obj.CustomerName :
                obj.Address = obj.CustomerName.address
        super().save_model(request, obj, form, change)