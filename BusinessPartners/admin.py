from django.contrib import admin
from django import forms
from .models import  BusinessPartner
from Sales.models import SalesOrderInfo,DeliveryInfo
from Purchasing.models import PurchaseOrderInfo
from django.db.models import Sum

class BusinessPartnerForm(forms.ModelForm):
    class Meta:
        model = BusinessPartner
        fields = ['code', 'currency_type','name','vendor_type','address']  # সব ফিল্ড অবশ্যই যোগ করুন

    # যেহেতু BusinessPartner মডেলে currency_type এবং vendor_type ফিল্ডের একটি choices ফিল্ড আছে, আমি এটি একটি রেডিও বাটন রুপে দেখাতে চাই
    currency_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BusinessPartner.CURRENCY_TYPES)
    vendor_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BusinessPartner.VENDOR_TYPES)

@admin.register(BusinessPartner)
class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_sales_amount','total_delivery_amount','total_purchase_amount')
    search_fields = ('name', 'code')
    list_filter = ('currency_type', 'vendor_type')
    ordering = ('name',)
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    form = BusinessPartnerForm 
    class Media:
        js = ('js/businesspartner.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }     
    def total_sales_amount(self, obj):
        # Calculate the sum of totalAmount for SalesOrderInfo related to this BusinessPartner
        total_amount = SalesOrderInfo.objects.filter(customerName=obj).aggregate(total_sales=Sum('totalAmount'))['total_sales']
        return total_amount or 0

    total_sales_amount.short_description = 'Order Amount'  
    
    def total_delivery_amount(self, obj):
        # Calculate the sum of totalAmount for SalesOrderInfo related to this BusinessPartner
        total_amount = DeliveryInfo.objects.filter(customerName=obj).aggregate(total_sales=Sum('totalAmount'))['total_sales']
        return total_amount or 0

    total_delivery_amount.short_description = 'Delivery Amount'    
    
    def total_purchase_amount(self, obj):
        # Calculate the sum of totalAmount for SalesOrderInfo related to this BusinessPartner
        total_amount = PurchaseOrderInfo.objects.filter(customerName=obj).aggregate(total_sales=Sum('totalAmount'))['total_sales']
        return total_amount or 0

    total_purchase_amount.short_description = 'Purchase Amount'          
    




