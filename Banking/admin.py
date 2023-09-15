from django.contrib import admin
from django import forms
from django.db import models
from .models import IncomingPaymentInfo,OutgoingPaymentInfo
# Register your models here.
class IncomingPaymentInfoAdminForm(forms.ModelForm):
    class Meta:
        model = IncomingPaymentInfo
        fields = ['customerName','docNo', 'totalAmount','remarks']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),            
            # 'customerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = IncomingPaymentInfo.objects.order_by('-docNo').first()
            if last_order:
                next_order_number = last_order.docNo + 1
            else:
                next_order_number = 1

            self.initial['docNo'] = next_order_number
            
@admin.register(IncomingPaymentInfo)
class IncomingPaymentInfoAdmin(admin.ModelAdmin):
    form = IncomingPaymentInfoAdminForm        
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    class Media:

        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }         
    
    
    
    
    
    
class OutgoingPaymentInfoAdminForm(forms.ModelForm):
    class Meta:
        model = OutgoingPaymentInfo
        fields = ['customerName','docNo', 'totalAmount','remarks']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),            
            # 'customerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = OutgoingPaymentInfo.objects.order_by('-docNo').first()
            if last_order:
                next_order_number = last_order.docNo + 1
            else:
                next_order_number = 1

            self.initial['docNo'] = next_order_number    
        
        
@admin.register(OutgoingPaymentInfo)
class OutgoingPaymentInfoAdmin(admin.ModelAdmin):
    form = OutgoingPaymentInfoAdminForm        
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'            
    
    class Media:

        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }     