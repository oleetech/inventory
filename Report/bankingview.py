from django.shortcuts import render
from .forms import SalesEmployeeForm
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from django.db.models import IntegerField
from datetime import datetime
import calendar
from django.db import models
from .forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter,ItemNameForm
from Banking.models import IncomingPaymentInfo,OutgoingPaymentInfo
#ডেট অনুযায়ী IncomingPaymentInfo রিপোর্ট 
def incoming_payment_info_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = IncomingPaymentInfo.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'banking/incoming_payment_info_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'banking/incoming_payment_info_between_date.html', {'form': form})


#ডেট অনুযায়ী IncomingPaymentInfo রিপোর্ট 
def outgoing_payment_info_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = OutgoingPaymentInfo.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'banking/outgoing_payment_info_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'banking/outgoing_payment_info_between_date.html', {'form': form})











