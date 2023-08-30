from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item



from .models import PurchaseOrderInfo, PurchaseItem
class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    form = PurchaseItemForm
    extra = 1

class PurchaseOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderInfo
        fields = '__all__'
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = PurchaseOrderInfo.objects.order_by('-docNo').first()
            if last_order:
                next_order_number = last_order.docNo + 1
            else:
                next_order_number = 1

            self.initial['docNo'] = next_order_number

@admin.register(PurchaseOrderInfo)
class PurchaseOrderInfoAdmin(admin.ModelAdmin):
    form = PurchaseOrderInfoAdminForm
    inlines = [PurchaseItemInline]

    class Media:
        js = ('js/purchaseorder.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        super().save_model(request, obj, form, change)
        
        
        
from .models import GoodsReceiptPoInfo, GoodsReceiptPoItem
class GoodsReceiptPoItemForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptPoItem
        fields = '__all__'

class GoodsReceiptPoItemInline(admin.TabularInline):
    model = GoodsReceiptPoItem
    form = GoodsReceiptPoItemForm
    extra = 1

class GoodsReceiptPoInfoAdminForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptPoInfo
        fields = '__all__'
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_receipt = GoodsReceiptPoInfo.objects.order_by('-docNo').first()
            if last_receipt:
                next_receipt_number = last_receipt.docNo + 1
            else:
                next_receipt_number = 1

            self.initial['docNo'] = next_receipt_number

@admin.register(GoodsReceiptPoInfo)
class GoodsReceiptPoInfoAdmin(admin.ModelAdmin):
    form = GoodsReceiptPoInfoAdminForm
    inlines = [GoodsReceiptPoItemInline]

    class Media:
        js = ('js/goodsreceiptpo.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        super().save_model(request, obj, form, change)

