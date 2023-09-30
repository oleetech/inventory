from django.contrib import admin
from django import forms
from django.db import models
from django.db.models import Sum


from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django_select2.forms import ModelSelect2Widget
from .models import SalesOrderInfo, SalesOrderItem,DeliveryInfo,DeliveryItem,AdditionalDeliveryData,ChallanReceivedDeliveryData
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item


def calculate_delivery(salesOrderNo):
    delivery_qty = DeliveryItem.objects.filter(orderNo=salesOrderNo).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0    
    return delivery_qty  

def calculate_delivery_balance(salesOrderNo):
    sales_order = SalesOrderInfo.objects.get(docNo=salesOrderNo)
    delivery_balance = sales_order.totalQty - calculate_delivery(salesOrderNo)
    return delivery_balance
    
class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  
    
'''
  ____            _                  _____                       _                               
 / ___|    __ _  | |   ___   ___    | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___ 
 \___ \   / _` | | |  / _ \ / __|   |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \
  ___) | | (_| | | | |  __/ \__ \   | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/
 |____/   \__,_| |_|  \___| |___/   |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___|
                                                        |_|                  |___/               

'''  
from .models import SalesEmployee      
@admin.register(SalesEmployee)
class SalesEmployeeAdmin(admin.ModelAdmin): 
    list_display = ('first_name','last_name', 'email', 'phone_number', 'hire_date','active','total_order_amount','total_delivery_amount','balance_amount')
    search_fields = ('first_name', )  
     
    def total_order_amount(self, obj):
        # Calculate the total sum of SalesOrderInfo.totalAmount for this SalesEmployee
        total_amount = SalesOrderInfo.objects.filter(sales_employee=obj).aggregate(total_amount=Sum('totalAmount'))['total_amount']
        return total_amount if total_amount is not None else 0
    total_order_amount.short_description = 'Total Order Amount'   
    
    def total_delivery_amount(self, obj):
        # Calculate the total sum of SalesOrderInfo.totalAmount for this SalesEmployee
        total_amount = DeliveryInfo.objects.filter(sales_employee=obj).aggregate(total_amount=Sum('totalAmount'))['total_amount']
        return total_amount if total_amount is not None else 0
    total_delivery_amount.short_description = 'Total Delivery Amount' 
    
    def balance_amount(self, obj):
        total_order_amount = self.total_order_amount(obj)
        total_delivery_amount = self.total_delivery_amount(obj)
        return total_order_amount - total_delivery_amount
    
    balance_amount.short_description = 'Balance Amount'    
           
    
'''
  ____            _                   ___               _               
 / ___|    __ _  | |   ___   ___     / _ \   _ __    __| |   ___   _ __ 
 \___ \   / _` | | |  / _ \ / __|   | | | | | '__|  / _` |  / _ \ | '__|
  ___) | | (_| | | | |  __/ \__ \   | |_| | | |    | (_| | |  __/ | |   
 |____/   \__,_| |_|  \___| |___/    \___/  |_|     \__,_|  \___| |_|   
                                                                        
'''
class SalesOrderItemForm(forms.ModelForm):
    class Meta:
        model = SalesOrderItem
        fields = ['code','name', 'uom','quantity','size','color','style','price','priceTotal','lineNo','description']
        widgets = {
            # 'ItemName': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains'])
        }

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    form = SalesOrderItemForm
    extra = 0

class SalesOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesOrderInfo
        fields = ['status','docNo','customerName', 'totalQty','sales_employee','totalAmount','remarks','edd']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),            
            'customerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = SalesOrderInfo.objects.order_by('-docNo').first()
            if last_order:
                next_order_number = last_order.docNo + 1
            else:
                next_order_number = 1

            self.initial['docNo'] = next_order_number
            
     
                    
@admin.register(SalesOrderInfo)
class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]
    list_display = ('docNo','customerName', 'totalAmount', 'totalQty', 'created', 'delivery_qty', 'deliveryBalance')
    search_fields = ('docNo', )    
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    readonly_fields = ('delivery_qty', 'deliveryBalance')  # Use field names instead of functions
    
    def delivery_qty(self, obj):
        return calculate_delivery(obj.docNo)

    delivery_qty.short_description = 'delivery'
    
    
    def deliveryBalance(self, obj):
        return calculate_delivery_balance(obj.docNo)

    deliveryBalance.short_description = 'deliveryBalance' 
    
           
    class Media:
        js = ('js/salesorder.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        } 
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName :
                obj.address = obj.customerName.address
        obj.owner = request.user if request.user.is_authenticated else None                         
        super().save_model(request, obj, form, change)
        

'''
  ____           _   _                               
 |  _ \    ___  | | (_) __   __   ___   _ __   _   _ 
 | | | |  / _ \ | | | | \ \ / /  / _ \ | '__| | | | |
 | |_| | |  __/ | | | |  \ V /  |  __/ | |    | |_| |
 |____/   \___| |_| |_|   \_/    \___| |_|     \__, |
                                               |___/ 
'''


class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['salesOrder','docNo','customerName', 'totalQty','address','totalAmount','sales_employee']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'customerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }

                
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = DeliveryInfo.objects.order_by('-docNo').first()
            if last_order:
                next_order_number = last_order.docNo + 1
            else:
                next_order_number = 1

            self.initial['docNo'] = next_order_number
            

    def clean(self):
        cleaned_data = super().clean()
        order_no = cleaned_data.get('salesOrder')
        total_qty = cleaned_data.get('totalQty')

        # Get the sum of previous DeliveryItem total quantities based on salesOrder
        previous_delivery_quantity = DeliveryInfo.objects.filter(salesOrder=order_no).exclude(pk=self.instance.pk).aggregate(Sum('totalQty'))['totalQty__sum'] or 0

        # Get the SalesOrderInfo for the given docNo
        sales_order_info = SalesOrderInfo.objects.filter(docNo=order_no).first()

        if sales_order_info:
            total_quantity = sales_order_info.totalQty

            # Calculate the total quantity including previous and current
            total_delivery_quantity = previous_delivery_quantity + total_qty

            if total_delivery_quantity  > total_quantity:
                raise forms.ValidationError("Total delivery quantity exceeds SalesOrderInfo total quantity.")
        
        return cleaned_data              
class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['receiptNo','lineNo','code','name', 'uom','quantity','size','color','price','priceTotal','orderNo','orderlineNo']        
        widgets = {
            'orderNo': forms.TextInput(attrs={'readonly': 'readonly'}),

            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'ItemName': DeliveryItemModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        }
        
        

            
class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 0  
    form = DeliveryItemForm
    
    
@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('docNo',  'totalQty','totalAmount')
    inlines = [DeliveryItemInline] 
    form = DeliveryInfoForm
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

  
        
    class Media:
        js = ('js/delivery.js',)
        defer = True         
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }         
     
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName :
                obj.address = obj.customerName.address
        obj.owner = request.user if request.user.is_authenticated else None            
                
        super().save_model(request, obj, form, change)
        

@admin.register(AdditionalDeliveryData)
class AdditionalDeliveryDataAdmin(admin.ModelAdmin):   
    list_display = ('delivery_info','delivertobuyerdate')
    search_fields = ('delivery_info__docNo', ) 
    
@admin.register(ChallanReceivedDeliveryData)
class ChallanReceivedDeliveryDataDataAdmin(admin.ModelAdmin):   
    list_display = ('delivery_info','challanreceiveddate')
    search_fields = ('delivery_info__docNo', )     
        
'''
  ____            _                   ___                    _            _     _                 
 / ___|    __ _  | |   ___   ___     / _ \   _   _    ___   | |_    ___  | |_  (_)   ___    _ __  
 \___ \   / _` | | |  / _ \ / __|   | | | | | | | |  / _ \  | __|  / _ \ | __| | |  / _ \  | '_ \ 
  ___) | | (_| | | | |  __/ \__ \   | |_| | | |_| | | (_) | | |_  |  __/ | |_  | | | (_) | | | | |
 |____/   \__,_| |_|  \___| |___/    \__\_\  \__,_|  \___/   \__|  \___|  \__| |_|  \___/  |_| |_|
'''
              
from .models import SalesQuotetionInfo, SalesQuotetionItem
class SalesQuotetionItemForm(forms.ModelForm):
    class Meta:
        model = SalesQuotetionItem
        fields = ['code','name', 'uom','quantity','price','priceTotal']   

class SalesQuotetionItemInline(admin.TabularInline):
    model = SalesQuotetionItem
    form = SalesQuotetionItemForm
    extra = 0

class SalesQuotetionInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesQuotetionInfo
        fields = ['customerName','docNo', 'totalQty','totalAmount','sales_employee']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_quotation = SalesQuotetionInfo.objects.order_by('-docNo').first()
            if last_quotation:
                next_quotation_number = last_quotation.docNo + 1
            else:
                next_quotation_number = 1

            self.initial['docNo'] = next_quotation_number

@admin.register(SalesQuotetionInfo)
class SalesQuotetionInfoAdmin(admin.ModelAdmin):
    form = SalesQuotetionInfoAdminForm
    inlines = [SalesQuotetionItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/salesquotetion.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        } 
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        obj.owner = request.user if request.user.is_authenticated else None               
        super().save_model(request, obj, form, change)

'''
  ____           _                          
 |  _ \    ___  | |_   _   _   _ __   _ __  
 | |_) |  / _ \ | __| | | | | | '__| | '_ \ 
 |  _ <  |  __/ | |_  | |_| | | |    | | | |
 |_| \_\  \___|  \__|  \__,_| |_|    |_| |_|
                                            

                                                                                                  
''' 
from django.contrib import admin
from .models import ReturnInfo, ReturnItem
from django import forms
from django_select2.forms import ModelSelect2Widget
from django.utils import timezone

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ['code','name', 'uom','quantity','price','priceTotal']   

class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    form = ReturnItemForm
    extra = 0

class ReturnInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ReturnInfo
        fields = ['customerName','docNo', 'totalQty','totalAmount','sales_employee']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_return = ReturnInfo.objects.order_by('-docNo').first()
            if last_return:
                next_return_number = last_return.docNo + 1
            else:
                next_return_number = 1

            self.initial['docNo'] = next_return_number

@admin.register(ReturnInfo)
class ReturnInfoAdmin(admin.ModelAdmin):
    form = ReturnInfoAdminForm
    inlines = [ReturnItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/returninfo.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        } 
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        obj.owner = request.user if request.user.is_authenticated else None              
        super().save_model(request, obj, form, change)


        
        
        
from .models import ARInvoiceInfo, ARInvoiceItem

class ARInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = ARInvoiceItem
        fields = ['code','name', 'uom','quantity','price','priceTotal','deliveryNo','deliverylineNo','lineNo','orderNo']   

class ARInvoiceItemInline(admin.TabularInline):
    model = ARInvoiceItem
    form = ARInvoiceItemForm
    extra = 0

class ARInvoiceInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ARInvoiceInfo
        fields = ['deliveryNo','salesOrder','customerName','docNo','address' ,'totalQty','totalAmount','sales_employee']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_invoice = ARInvoiceInfo.objects.order_by('-docNo').first()
            if last_invoice:
                next_invoice_number = last_invoice.docNo + 1
            else:
                next_invoice_number = 1

            self.initial['docNo'] = next_invoice_number

@admin.register(ARInvoiceInfo)
class ARInvoiceInfoAdmin(admin.ModelAdmin):
    form = ARInvoiceInfoAdminForm
    inlines = [ARInvoiceItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/arinvoice.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        } 
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        obj.owner = request.user if request.user.is_authenticated else None              
        super().save_model(request, obj, form, change)
        

        
        
   