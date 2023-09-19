from django.shortcuts import render
from .forms import SalesEmployeeForm
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from django.db.models import IntegerField
from datetime import datetime
import calendar
from django.db import models
from .forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter,ItemNameForm
from Purchasing.models import PurchaseQuotetionInfo,PurchaseQuotetionItem,PurchaseOrderInfo,PurchaseItem,GoodsReceiptPoInfo,GoodsReceiptPoItem,ApInvoiceInfo,ApInvoiceItem
'''
  ____                          _                               ___                    _             _     _                 
 |  _ \   _   _   _ __    ___  | |__     __ _   ___    ___     / _ \   _   _    __ _  | |_    __ _  | |_  (_)   ___    _ __  
 | |_) | | | | | | '__|  / __| | '_ \   / _` | / __|  / _ \   | | | | | | | |  / _` | | __|  / _` | | __| | |  / _ \  | '_ \ 
 |  __/  | |_| | | |    | (__  | | | | | (_| | \__ \ |  __/   | |_| | | |_| | | (_| | | |_  | (_| | | |_  | | | (_) | | | | |
 |_|      \__,_| |_|     \___| |_| |_|  \__,_| |___/  \___|    \__\_\  \__,_|  \__,_|  \__|  \__,_|  \__| |_|  \___/  |_| |_|
                                                                                                                             

'''

#ডেট অনুযায়ী purchase_quotation রিপোর্ট 
def purchase_quotation_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = PurchaseQuotetionItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'purchase/purchase_quotation_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'purchase/purchase_quotation_between_date.html', {'form': form})



#ডেট অনুযায়ী purchase_order রিপোর্ট 
def purchase_order_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = PurchaseItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'purchase/purchase_order_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'purchase/purchase_order_between_date.html', {'form': form})


#ডেট অনুযায়ী goods_receipt_po রিপোর্ট 
def goods_receipt_po_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = GoodsReceiptPoItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'purchase/goods_receipt_po_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'purchase/goods_receipt_po_between_date.html', {'form': form})



#ডেট অনুযায়ী Ap Invoice রিপোর্ট 
def ap_invoice_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ApInvoiceItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'purchase/ap_invoice_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'purchase/ap_invoice_between_date.html', {'form': form})

#ডেট অনুযায়ী Ap Invoice রিপোর্ট 
def ap_invoice_between_date_without_item(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ApInvoiceInfo.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'purchase/ap_invoice_between_date_without_item.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'purchase/ap_invoice_between_date_without_item.html', {'form': form})