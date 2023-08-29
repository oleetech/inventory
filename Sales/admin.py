from django.contrib import admin
from django import forms
from django_select2.forms import ModelSelect2Widget
from .models import SalesOrderInfo, SalesOrderItem 
from BusinessPartners.models import BusinessPartner
from ItemMasterData.models import Item

from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO



def generate_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    for order_info in queryset:
        p.drawString(100, 700, f"Order Number: {order_info.OrderNumber}")
        p.drawString(100, 680, f"Customer: {order_info.CustomerName}")
        p.drawString(100, 660, f"Address: {order_info.Address}")
        # Calculate the y-coordinate for the table's top
        y = 600        
        data = []
        total_amount = 0

        for item in SalesOrderItem.objects.filter(OrderNumber=order_info):
            data.append([item.ItemName, item.Quantity, item.Price, item.PriceTotal])
            total_amount += item.PriceTotal
        
        # Create a table
        table = Table(data, colWidths=[150, 80, 80, 80])
        
        # Apply table style
        table_style = TableStyle([

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),
            ('LINEABOVE', (0, -1), (-1, -1), 1, (0, 0, 0)),
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
        ])
        table.setStyle(table_style)

        # Draw the table on the canvas
        table.wrapOn(p, 400, 600)
        table.drawOn(p, 100, y)
        
        p.drawString(100, 460, f"Total Amount: {total_amount}")
        p.showPage()

    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

generate_pdf.short_description = "Generate PDF"

class CustomModelSelect2Widget(ModelSelect2Widget):
    def label_from_instance(self, obj):
        return obj.name  

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
            'OrderNumber': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'CustomerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_order = SalesOrderInfo.objects.order_by('-OrderNumber').first()
            if last_order:
                next_order_number = last_order.OrderNumber + 1
            else:
                next_order_number = 1

            self.initial['OrderNumber'] = next_order_number
            
                    
@admin.register(SalesOrderInfo)
class SalesOrderInfoAdmin(admin.ModelAdmin):
    form = SalesOrderInfoAdminForm
    inlines = [SalesOrderItemInline]
    
    actions = [generate_pdf]
        
    class Media:
        js = ('js/salesorder.js',)
        defer = True

    def save_model(self, request, obj, form, change):
        if not obj.Address:
            if obj.CustomerName :
                obj.Address = obj.CustomerName.address
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
        fields = ['DocNo','SalesOrder','CustomerName','Address','TotalAmount','TotalQty']
        widgets = {
            'DocNo': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            'TotalQty': forms.TextInput(attrs={'readonly': 'readonly'}),
            'CustomerName': CustomModelSelect2Widget(model=BusinessPartner, search_fields=['name__icontains']),
        }
class DeliveryItemForm(forms.ModelForm):
    class Meta:
        model = DeliveryItem
        fields = ['ItemName','Quantity','Price','PriceTotal']
        widgets = {

            'TotalAmount': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'ItemName': DeliveryItemModelSelect2Widget(model=Item, search_fields=['name__icontains']),
        }
class DeliveryItemInline(admin.TabularInline):
    model = DeliveryItem
    extra = 1  
    form = DeliveryItemForm
    
    
@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ('DocNo',  'TotalQty','TotalAmount')
    inlines = [DeliveryItemInline] 
    form = DeliveryInfoForm
  
  
        
    class Media:
        js = ('js/delivery.js',)
        defer = True         
        
     
    def save_model(self, request, obj, form, change):
        if not obj.Address:
            if obj.CustomerName :
                obj.Address = obj.CustomerName.address
        super().save_model(request, obj, form, change)