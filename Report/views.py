from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from datetime import datetime
import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from Production.models import BillOfMaterials, ChildComponent,Production, ProductionComponent,ProductionReceipt,ProductionReceiptItem
from .forms import DateFilterForm


    
    
def receipt_from_production_between_date(request):
    form = DateFilterForm(request.GET)
    
    if request.method == 'GET' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ProductionReceiptItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'receipt_from_production_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'receipt_from_production_between_date.html', {'form': form})
