from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.db.models import Sum
from datetime import datetime
import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from Production.models import BillOfMaterials, ChildComponent,Production, ProductionComponent,ProductionReceipt,ProductionReceiptItem
from .forms import DateFilterForm,OrderFilterForm
from .models import Post
def index(request):
    # Get the first record of the Post model.
    post = Post.objects.first()

    # Get the content of the first record.
    content = post.content

    context = {
        'content': content,
    }

    return render(request, 'index.html', context)
    return render(request, 'index.html', context)
    
    
def receipt_from_production_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
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

def receipt_from_production_based_on_order_no(request):
    form = OrderFilterForm(request.POST)  # Initialize form whether it's a POST or GET request
    
    if request.method == 'POST' and form.is_valid():
        order_no = form.cleaned_data['orderNo']
        
        # Retrieve ProductionReceiptItems based on the salesOrder
        receipt_items = ProductionReceiptItem.objects.filter(salesOrder=order_no)
        
        return render(request, 'receipt_from_production_based_on_order_no.html', {'form': form, 'items': receipt_items})
    
    return render(request, 'receipt_from_production_based_on_order_no.html', {'form': form})


def total_quantity_by_department(request):
    form = OrderFilterForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order_no = form.cleaned_data['orderNo']

        # Retrieve total quantity grouped by department based on the salesOrder
        quantity_by_department = ProductionReceiptItem.objects.filter(salesOrder=order_no).values('department').annotate(total_quantity=Sum('quantity'))

        return render(request, 'total_quantity_by_department.html', {'form': form, 'quantity_by_department': quantity_by_department})

    return render(request, 'total_quantity_by_department.html', {'form': form})