from django.contrib import admin
from django.db import models
from django import forms
from .models import Warehouse, Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery

from django_select2.forms import ModelSelect2Widget
class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  # Replace 'name' with the appropriate field
    
def calculate_instock(item):
    stock_quantity = Stock.objects.filter(item=item).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    receipt_quantity = ItemReceipt.objects.filter(item=item).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    delivery_quantity = ItemDelivery.objects.filter(item=item).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    instock = stock_quantity + receipt_quantity - delivery_quantity
    return instock

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'instock', 'description', 'price', 'warehouse')
    readonly_fields = ('instock',)
    search_fields = ('name',)  

    def instock(self, obj):
        return calculate_instock(obj)

    instock.short_description = 'In Stock'
    
class ItemReceiptinfoForm(forms.ModelForm):
    class Meta:
        model = ItemReceiptinfo
        fields = ['docno',]
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }    
class ItemReceiptInlineForm(forms.ModelForm):
    class Meta:
        model = ItemReceipt
        fields = ['item','quantity']
        widgets = {
            'item': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        } 
class ItemReceiptInline(admin.TabularInline):
    model = ItemReceipt
    extra = 1
    form = ItemReceiptInlineForm



@admin.register(ItemReceiptinfo)
class ItemReceiptinfoAdmin(admin.ModelAdmin):
    inlines = [ItemReceiptInline]
    form = ItemReceiptinfoForm
    
    
class ItemDeliveryinfoForm(forms.ModelForm):
    class Meta:
        model = ItemDeliveryinfo
        fields = ['docno',]
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
        
class ItemDeliveryInlineForm(forms.ModelForm):
    class Meta:
        model = ItemDelivery
        fields = ['item','quantity']
        widgets = {
            'item': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        } 
        
              
class ItemDeliveryInline(admin.TabularInline):
    model = ItemDelivery
    extra = 1
    form = ItemDeliveryInlineForm


@admin.register(ItemDeliveryinfo)
class ItemDeliveryinfoAdmin(admin.ModelAdmin):
    inlines = [ItemDeliveryInline]
    form =  ItemDeliveryinfoForm

@admin.register(Warehouse)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location') 

@admin.register(Stock)
class PostAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    search_fields = ('item', ) 
