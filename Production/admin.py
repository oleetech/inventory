from django.contrib import admin
from django import forms
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


from django.core.exceptions import ValidationError

from ItemMasterData.models import Item
from GeneralSettings.models import Unit
from django_select2.forms import ModelSelect2Widget
# Register your models here.
from .models import BillOfMaterials, ChildComponent

class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  # Replace 'name' with the appropriate field
    
class CustomModelSelect2Widgetd(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.OrderNumber  # Replace 'name' with the appropriate field    
'''
  ____    _   _   _      ___     __     __  __           _                   _           _       
 | __ )  (_) | | | |    / _ \   / _|   |  \/  |   __ _  | |_    ___   _ __  (_)   __ _  | |  ___ 
 |  _ \  | | | | | |   | | | | | |_    | |\/| |  / _` | | __|  / _ \ | '__| | |  / _` | | | / __|
 | |_) | | | | | | |   | |_| | |  _|   | |  | | | (_| | | |_  |  __/ | |    | | | (_| | | | \__ \
 |____/  |_| |_| |_|    \___/  |_|     |_|  |_|  \__,_|  \__|  \___| |_|    |_|  \__,_| |_| |___/
                                                                                                 
'''    
class ChildComponentForm(forms.ModelForm):
    class Meta:
        model = ChildComponent
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
        }  
class ChildComponentInline(admin.TabularInline):
    model = ChildComponent
    extra = 0 
    form = ChildComponentForm  



class BillOfMaterialsAdminForm(forms.ModelForm):
    class Meta:
        model = BillOfMaterials
        fields = ['code','name','quantity','uom']
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
@admin.register(BillOfMaterials)                     
class BillOfMaterialsAdmin(admin.ModelAdmin):
    inlines = [ChildComponentInline]   
    form = BillOfMaterialsAdminForm  
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    class Media: 
        js = ('js/billofmaterials.js','bootstrap.bundle.min.js','js/dataTables.min.js')
        defer = True  # Add the defer attribute          
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css','css/dataTables.min.css'),
        }      
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)     

        
     
             



'''
  ____                       _                  _     _                      ___               _               
 |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __      / _ \   _ __    __| |   ___   _ __ 
 | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \    | | | | | '__|  / _` |  / _ \ | '__|
 |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |   | |_| | | |    | (_| | |  __/ | |   
 |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|    \___/  |_|     \__,_|  \___| |_|   
                                                                                                               
'''
from .models import Production, ProductionComponent
from Sales.models import SalesOrderInfo,SalesOrderItem

 
    
class ProductionForm(forms.ModelForm):
    # docno = forms.IntegerField(disabled=True)  # Add this line to the form

    
    class Meta:
        model = Production
        fields = ['status','docno','code',   'salesOrder','name', 'owner','quantity','uom','remarks']
        widgets = {
            'owner': forms.TextInput(attrs={'readonly': 'readonly'}),
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = Production.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno

class  ProductionComponentInlineForm(forms.ModelForm) :
    class Meta:
        model = ProductionComponent
        fields = ['code','name','uom','quantity','lineNo' ]
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }

            
            
class ProductionComponentInline(admin.TabularInline):
    model = ProductionComponent
    extra = 0  
    form = ProductionComponentInlineForm   
@admin.register(Production)             
class ProductionAdmin(admin.ModelAdmin):
    form = ProductionForm
    inlines = [ProductionComponentInline]
    list_display = ('docno','salesOrder','name','quantity' )
    search_fields = ('salesOrder', )  

    change_form_template = 'admin/Production/ProductionOrder/change_form.html'      
    class Media:
        js = ('js/productionorder.js',)
        defer = True  # Add the defer attribute
        
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }     
        
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)          

'''
  ____                         _           _       _____                                ____                       _                  _     _                 
 |  _ \    ___    ___    ___  (_)  _ __   | |_    |  ___|  _ __    ___    _ __ ___     |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __  
 | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|   | |_    | '__|  / _ \  | '_ ` _ \    | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_    |  _|   | |    | (_) | | | | | | |   |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |
 |_| \_\  \___|  \___|  \___| |_| | .__/   \__|   |_|     |_|     \___/  |_| |_| |_|   |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|
                                  |_|                                                                                                                         
'''
from .models import ProductionReceipt,ProductionReceiptItem
class ProductionReceiptForm(forms.ModelForm):
    docno = forms.IntegerField(disabled=True)  # Add this line to the form


    
    class Meta:
        model = ProductionReceipt
        fields = ['department','docno','created']
        widgets = {
            'docno': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        if not self.instance.pk:
            # Get the last inserted docno
            last_docno = ProductionReceipt.objects.order_by('-docno').first()
            if last_docno:
                next_docno = last_docno.docno + 1
            else:
                next_docno = 1

            self.initial['docno'] = next_docno

class  ProductionReceiptItemInlineForm(forms.ModelForm) :

    class Meta:
        model = ProductionReceiptItem
        fields = ['productionNo','orderlineNo','code','name','uom','quantity','size','color','price','priceTotal','salesOrder','lineNo' ]
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            
        }
      
                
class ProductionReceiptItemInline(admin.TabularInline):
    model = ProductionReceiptItem
    extra = 0  
    form = ProductionReceiptItemInlineForm   
@admin.register(ProductionReceipt) 
class ProductionReceiptAdmin(admin.ModelAdmin):
    inlines = [ProductionReceiptItemInline]
    form =   ProductionReceiptForm  
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'   
    list_display = ('docno','department' )
    search_fields = ('docno', )         
    class Media:
        js = ('js/receiptfromproduction.js','js/library/bootstrap.bundle.min.js','js/library/dataTables.min.js')
        defer = True  # Add the defer attribute    
        
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css','css/bootstrap.min.css'),
        }   
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)            