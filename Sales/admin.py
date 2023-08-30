from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import SalesOrderInfo, SalesOrderItem 
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item


    
class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  
    
    
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
        fields = '__all__'
        widgets = {
            # 'ItemName': CustomModelSelect2Widget(model=Item, search_fields=['name__icontains'])
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
    list_display = ('docNo','customerName', 'totalAmount', 'totalQty')
    search_fields = ('docNo', )    


        
    class Media:
        js = ('js/salesorder.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName :
                obj.address = obj.customerName.address
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
        fields = ['docNo','customerName','address','totalAmount','totalQty']
        widgets = {
            'docNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'totalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'customerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['name','quantity','price','priceTotal']
        widgets = {

            'totalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'ItemName': DeliveryItemModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        }
class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1  
    form = DeliveryItemForm
    
    
@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('docNo',  'totalQty','totalAmount')
    inlines = [DeliveryItemInline] 
    form = DeliveryInfoForm

  
        
    class Media:
        js = ('js/delivery.js',)
        defer = True         
        
     
    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName :
                obj.address = obj.customerName.address
        super().save_model(request, obj, form, change)
        
        
        
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
        fields = '__all__'

class SalesQuotetionItemInline(admin.TabularInline):
    model = SalesQuotetionItem
    form = SalesQuotetionItemForm
    extra = 1

class SalesQuotetionInfoAdminForm(forms.ModelForm):
    class Meta:
        model = SalesQuotetionInfo
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

    class Media:
        js = ('js/salesquotetion.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
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
        fields = '__all__'

class ReturnItemInline(admin.TabularInline):
    model = ReturnItem
    form = ReturnItemForm
    extra = 1

class ReturnInfoAdminForm(forms.ModelForm):
    class Meta:
        model = ReturnInfo
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

    class Media:
        js = ('js/returninfo.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.address:
            if obj.customerName:
                obj.address = obj.customerName.address
        super().save_model(request, obj, form, change)


        
        
        
        
        
        
        
        
        