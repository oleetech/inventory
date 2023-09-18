from django.contrib import admin
from django.db import models
from django import forms
from .models import Warehouse, ItemGroup,Item, Stock, ItemReceiptinfo, ItemReceipt, ItemDeliveryinfo, ItemDelivery,IssueForProductionInfo,IssueForProductionItem,LedgerEntry
from Purchasing.models import GoodsReceiptPoItem,GoodsReturnItem,PurchaseItem
from Production.models import Production,ProductionComponent
from Sales.models import SalesOrderItem,DeliveryItem
from django.db.models import Sum
import csv
from django.core.exceptions import ValidationError
from collections import defaultdict
from django.forms import BaseInlineFormSet

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
    issue_for_production= IssueForProductionItem.objects.filter(code=code).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
    instock = stock_quantity + purchase_order_goods_receipt + receipt_quantity - delivery_quantity - purchase_order_goods_return - issue_for_production
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

@admin.register(ItemGroup)
class ItemGroupAdmin(admin.ModelAdmin):
    list_display = ('name',  'description')
           
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code','name',  'description', 'price', 'instock','total_sales_quantity','total_delivery_quantity','total_purchase_quantity')
    readonly_fields = ('instock',)
    search_fields = ('name',) 
    fields = ['code','name','unit','price','item_group']  
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
        fields = ['department','docno']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'owner': forms.TextInput(attrs={'readonly': 'readonly'}),

            
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
        fields = ['code','name', 'uom','quantity']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
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
        fields = ['department','docno']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'owner': forms.TextInput(attrs={'readonly': 'readonly'}),

            
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
        fields = ['code','name', 'uom','quantity']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
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
        
        
                   
# @admin.register(Warehouse)
# class Warehouse(admin.ModelAdmin):
#     list_display = ('name', 'location')
#     search_fields = ('name', 'location') 
#     def save_model(self, request, obj, form, change):

#         obj.owner = request.user if request.user.is_authenticated else None
          
#         super().save_model(request, obj, form, change)  
         
class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['code','name', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),

            
        }        
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('code', 'name','quantity')
    search_fields = ('code','name' ) 
    fields=['code','name','quantity']
    form= StockForm
    class Media:
        js = ('js/stock.js',)
        defer = True  # Add the defer attribute    
        
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css','css/bootstrap.min.css'),
        }     
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
        if not obj.pk:  # Check if this is a new instance
            # Get the last inserted docno
            last_stock = Stock.objects.order_by('-docNo').first()
            if last_stock:
                obj.docNo = last_stock.docNo + 1
            else:
                obj.docNo = 1        
        super().save_model(request, obj, form, change)  
        

class IssueForProductionInfoForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form


    
    class Meta:
        model = IssueForProductionInfo
        fields = ['department','docno','created']
        widgets = {

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = IssueForProductionInfo.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno           
        
class  IssueForProductionItemInlineForm(forms.ModelForm) :
    
    class Meta:
        model = IssueForProductionItem
        fields = ['productionNo','orderlineNo','code','name','quantity','uom','lineNo','salesOrder' ]
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),

            
        }          







# class CustomIssueForProductionItemFormSet(BaseInlineFormSet):
#     def clean(self):
#         super().clean()
#         production_component_codes = defaultdict(dict)
#         issue_total_quantity = defaultdict(lambda: defaultdict(int))

#         # Gather all IssueForProductionItem records for the same productionNo and code
#         issue_items = IssueForProductionItem.objects.filter(
#             productionNo__in=[form.cleaned_data['productionNo'] for form in self.forms if not form.cleaned_data.get('DELETE')],
#             code__in=[form.cleaned_data['code'] for form in self.forms if not form.cleaned_data.get('DELETE')]
#         )

#         # Gather all ProductionComponent items for the same docNo
#         production_component_dict = {}
#         production_no_list = list(set([form.cleaned_data['productionNo'] for form in self.forms if not form.cleaned_data.get('DELETE')]))
#         production_components = ProductionComponent.objects.filter(
#             docNo__in=production_no_list
#         )
#         for pc in production_components:
#             if pc.docNo not in production_component_dict:
#                 production_component_dict[pc.docNo] = {}
#             production_component_dict[pc.docNo][pc.code] = {
#                 'quantity': pc.quantity,
#             }

#         for form in self.forms:
#             if not form.cleaned_data.get('DELETE'):
#                 production_no = form.cleaned_data.get('productionNo')
#                 code = form.cleaned_data.get('code')
#                 quantity = form.cleaned_data.get('quantity')

#                 # Get the total production quantity for the current code and docNo
#                 total_production_quantity = production_component_dict.get(production_no, {}).get(code, {}).get('quantity', 0)

#                 # Calculate the total issue quantity for the current code and docNo
#                 issue_total_quantity[production_no][code] = sum(
#                     issue_item.quantity for issue_item in issue_items if issue_item.code == code
#                 )

#                 # Check if the total issue quantity plus the current code quantity exceeds production quantity
#                 if total_production_quantity is not None and issue_total_quantity[production_no][code] + quantity > total_production_quantity:
#                     form.add_error('quantity', f"Total issue quantity for code {code} exceeds total production quantity for productionNo {production_no}.")
#                     raise ValidationError("Total issue quantity exceeds production quantity. Form submission aborted.")


class IssueForProductionItemInline(admin.TabularInline):
    model = IssueForProductionItem
    extra = 0  
    form = IssueForProductionItemInlineForm   
    # formset = CustomIssueForProductionItemFormSet
    
              
  
@admin.register(IssueForProductionInfo) 
class IssueForProductionInfoAdmin(admin.ModelAdmin):   
    inlines = [IssueForProductionItemInline]
    form =   IssueForProductionInfoForm  
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'   
    class Media:
        js = ('js/issueforproduction.js','js/library/bootstrap.bundle.min.js','js/library/dataTables.min.js')
        defer = True  # Add the defer attribute    
        
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css','css/bootstrap.min.css'),
        }         
        
@admin.register(LedgerEntry)         
class LedgerEntryAdmin(admin.ModelAdmin):  
     
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Check if this is a new instance
            # Get the last inserted docno
            last_ledger_entry = LedgerEntry.objects.order_by('-docNo').first()
            if last_ledger_entry:
                obj.docNo = last_ledger_entry.docNo + 1
            else:
                obj.docNo = 1

        super().save_model(request, obj, form, change)
