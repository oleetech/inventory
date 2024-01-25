from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item

from .models import PurchaseQuotetionInfo, PurchaseQuotetionItem
class PurchaseQuotetionItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseQuotetionItem
        fields = ['code','name', 'uom','quantity','price','priceTotal','lineNo']   

class PurchaseQuotetionItemInline(admin.TabularInline):
    model = PurchaseQuotetionItem
    form = PurchaseQuotetionItemForm
    extra = 0

class PurchaseQuotetionInfoAdminForm(forms.ModelForm):
    class Meta:
        model = PurchaseQuotetionInfo
        fields = ['customerName','docNo', 'totalQty','totalAmount']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_quotation = PurchaseQuotetionInfo.objects.order_by('-docNo').first()
            if last_quotation:
                next_quotation_number = last_quotation.docNo + 1
            else:
                next_quotation_number = 1

            self.initial['docNo'] = next_quotation_number

@admin.register(PurchaseQuotetionInfo)
class PurchaseQuotetionInfoAdmin(admin.ModelAdmin):
    form = PurchaseQuotetionInfoAdminForm
    inlines = [PurchaseQuotetionItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/purchasequotetion.js',)
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

from .models import PurchaseOrderInfo, PurchaseItem
class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['code','name', 'uom','quantity','price','priceTotal','lineNo']   

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    form = PurchaseItemForm
    extra = 0

class PurchaseOrderInfoAdminForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderInfo
        fields = ['customerName','docNo', 'totalQty','totalAmount']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'owner': forms.TextInput(attrs={'readonly': 'readonly'}),            
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
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/purchaseorder.js',)
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
        
        
        
from .models import GoodsReceiptPoInfo, GoodsReceiptPoItem
class GoodsReceiptPoItemForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptPoItem
        fields = ['purchareOrderNo','lineNo','code','name','uom','quantity','price','priceTotal']

class GoodsReceiptPoItemInline(admin.TabularInline):
    model = GoodsReceiptPoItem
    form = GoodsReceiptPoItemForm
    extra = 0

class GoodsReceiptPoInfoAdminForm(forms.ModelForm):
    class Meta:
        model = GoodsReceiptPoInfo
        fields = ['purchaseOrder','docNo','customerName','created','address','totalQty','totalAmount']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
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
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/goodsreceiptpo.js',)
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



from .models import GoodsReturnInfo, GoodsReturnItem

    
    
class GoodsReturnItemForm(forms.ModelForm):
    class Meta:
        model = GoodsReturnItem
        fields = '__all__'

class GoodsReturnItemInline(admin.TabularInline):
    model = GoodsReturnItem
    form = GoodsReturnItemForm
    extra = 0

class GoodsReturnInfoAdminForm(forms.ModelForm):
    class Meta:
        model = GoodsReturnInfo
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
            last_return = GoodsReturnInfo.objects.order_by('-docNo').first()
            if last_return:
                next_return_number = last_return.docNo + 1
            else:
                next_return_number = 1

            self.initial['docNo'] = next_return_number

@admin.register(GoodsReturnInfo)
class GoodsReturnInfoAdmin(admin.ModelAdmin):
    form = GoodsReturnInfoAdminForm
    inlines = [GoodsReturnItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/goodsreturn.js',)
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
        
        
        
        
from .models import ApInvoiceInfo, ApInvoiceItem

class ApInvoiceItemForm(forms.ModelForm):
    class Meta:
        model = ApInvoiceItem
        fields = '__all__'

class ApInvoiceItemInline(admin.TabularInline):
    model = ApInvoiceItem
    form = ApInvoiceItemForm
    extra = 0

class ApInvoiceInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ApInvoiceInfo
        fields = ['goodsreReiptNo','docNo','customerName', 'totalQty','totalAmount']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'customerName': ModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_invoice = ApInvoiceInfo.objects.order_by('-docNo').first()
            if last_invoice:
                next_invoice_number = last_invoice.docNo + 1
            else:
                next_invoice_number = 1

            self.initial['docNo'] = next_invoice_number

@admin.register(ApInvoiceInfo)
class ApInvoiceInfoAdmin(admin.ModelAdmin):
    form = ApInvoiceInfoAdminForm
    inlines = [ApInvoiceItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     

    class Media:
        js = ('js/apinvoice.js',)
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
        