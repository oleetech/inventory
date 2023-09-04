from django.contrib import admin
from django.db import models
from django import forms
from .models import Warehouse, Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery
from Purchasing.models import GoodsReceiptPoItem,GoodsReturnItem
from django_select2.forms import ModelSelect2Widget
class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  # Replace 'name' with the appropriate field
    


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',  'description', 'price', 'warehouse')

    search_fields = ('name',)  


    
class ItemReceiptinfoForm(forms.ModelForm):
    class Meta:
        model = ItemReceiptinfo
        fields = '__all__'
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }    
class ItemReceiptInlineForm(forms.ModelForm):
    class Meta:
        model = ItemReceipt
        fields = ['code','name', 'uom','quantity','price','priceTotal']
        widgets = {
        } 
class ItemReceiptInline(admin.TabularInline):
    model = ItemReceipt
    extra = 1
    form = ItemReceiptInlineForm



@admin.register(ItemReceiptinfo)
class ItemReceiptinfoAdmin(admin.ModelAdmin):
    inlines = [ItemReceiptInline]
    form = ItemReceiptinfoForm
    
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    class Media:   
        js = ('js/itemreceipt.js',)
        defer = True
                
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }      
class ItemDeliveryinfoForm(forms.ModelForm):
    class Meta:
        model = ItemDeliveryinfo
        fields = '__all__'
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
        
class ItemDeliveryInlineForm(forms.ModelForm):
    class Meta:
        model = ItemDelivery
        fields = ['code','name', 'uom','quantity','price','priceTotal']
        widgets = {
            
        } 
        
              
class ItemDeliveryInline(admin.TabularInline):
    model = ItemDelivery
    extra = 1
    form = ItemDeliveryInlineForm


@admin.register(ItemDeliveryinfo)
class ItemDeliveryinfoAdmin(admin.ModelAdmin):
    inlines = [ItemDeliveryInline]
    form =  ItemDeliveryinfoForm
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    class Media:   
        js = ('js/itemdelivery.js',)
        defer = True
                        
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }  
@admin.register(Warehouse)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location') 

@admin.register(Stock)
class PostAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    search_fields = ('item', ) 
