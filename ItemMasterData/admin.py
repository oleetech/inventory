from django.contrib import admin
from django.db import models
from django import forms
from .models import Warehouse, Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery
from Purchasing.models import GoodsReceiptPoItem,GoodsReturnItem,PurchaseItem
from Sales.models import SalesOrderItem,DeliveryItem
from django.db.models import Sum
import csv

from django_select2.forms import ModelSelect2Widget
class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  # Replace 'name' with the appropriate field
    
def calculate_instock(code):
    stock_quantity = Stock.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    receipt_quantity = ItemReceipt.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    delivery_quantity = ItemDelivery.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    purchase_order_goods_receipt = GoodsReceiptPoItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    purchase_order_goods_return = GoodsReturnItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    instock = stock_quantity + purchase_order_goods_receipt + receipt_quantity - delivery_quantity - purchase_order_goods_return
    return instock

# class ReadOnlyWidget(forms.Widget):
#     def render(self, name, value, attrs=None, renderer=None):
#         return value
    
# class ItemForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         super(ItemForm, self).__init__(*args, **kwargs)
#         instance = kwargs.get('instance')
#         if instance:
#             self.fields['instock'] = forms.CharField(
#                 widget=ReadOnlyWidget(attrs={'readonly': 'readonly'}),
#                 initial=calculate_instock(instance.code)
#             )

#     class Meta:
#         model = Item
#         fields = ['code','unit','name','warehouse','price']
#         widgets = {
#             'instock': forms.TextInput(attrs={'readonly': 'readonly'}),
#         }
#     class Media:   
                
#         css = {
#             'all': ('css/bootstrap.min.css','css/admin_styles.css'),
#         }          
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',  'description', 'price', 'warehouse','instock','total_sales_quantity','total_delivery_quantity','total_purchase_quantity')
    readonly_fields = ('instock',)
    search_fields = ('name',) 
    # form = ItemForm     
    # change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
   
    def total_sales_quantity(self,obj):
        # Calculate the total sum of SalesOrderItem.quantity for this Item's code
        total_quantity = SalesOrderItem.objects.filter(code=obj.code).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        # Handle the case where there are no related SalesOrderItem instances
        return total_quantity if total_quantity is not None else 0
    total_sales_quantity.short_description = 'Order Qty'  
    
    def total_delivery_quantity(self,obj):
        # Calculate the total sum of SalesOrderItem.quantity for this Item's code
        total_quantity = DeliveryItem.objects.filter(code=obj.code).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        # Handle the case where there are no related SalesOrderItem instances
        return total_quantity if total_quantity is not None else 0
    total_delivery_quantity.short_description = 'Delivery Qty'      
    
    def total_purchase_quantity(self,obj):
        # Calculate the total sum of SalesOrderItem.quantity for this Item's code
        total_quantity = PurchaseItem.objects.filter(code=obj.code).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        # Handle the case where there are no related SalesOrderItem instances
        return total_quantity if total_quantity is not None else 0
    total_purchase_quantity.short_description = 'Purchase Qty'      
        
    def instock(self, obj):
        return calculate_instock(obj.code)

    instock.short_description = 'In Stock'
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)  
        
        
           
    
class ItemReceiptinfoForm(forms.ModelForm):
    class Meta:
        model = ItemReceiptinfo
        fields = '__all__'
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        } 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = ItemReceiptinfo.objects.order_by('-docno').first()
            if last_order:
                next_order_number = last_order.docno + 1
            else:
                next_order_number = 1

            self.initial['docno'] = next_order_number           
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
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)               
class ItemDeliveryinfoForm(forms.ModelForm):
    class Meta:
        model = ItemDeliveryinfo
        fields = '__all__'
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = ItemDeliveryinfo.objects.order_by('-docno').first()
            if last_order:
                next_order_number = last_order.docno + 1
            else:
                next_order_number = 1

            self.initial['docno'] = next_order_number
                    
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
      
    def save_model(self, request, obj, form, change):
       

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)  
        
        
                   
@admin.register(Warehouse)
class Warehouse(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location') 
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)   
        
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')
    search_fields = ('item', ) 
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)     