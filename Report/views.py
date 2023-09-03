from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from django.db.models import IntegerField
from datetime import datetime
import calendar

import os
import pandas as pd
import matplotlib.pyplot as plt

from django.views.decorators.csrf import csrf_exempt
from Production.models import BillOfMaterials, ChildComponent,Production, ProductionComponent,ProductionReceipt,ProductionReceiptItem
from .forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter
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
    
'''
            ____                       _                  _     _                     ____                                  _   
            |  _ \   _ __    ___     __| |  _   _    ___  | |_  (_)   ___    _ __     |  _ \    ___   _ __     ___    _ __  | |_ 
            | |_) | | '__|  / _ \   / _` | | | | |  / __| | __| | |  / _ \  | '_ \    | |_) |  / _ \ | '_ \   / _ \  | '__| | __|
            |  __/  | |    | (_) | | (_| | | |_| | | (__  | |_  | | | (_) | | | | |   |  _ <  |  __/ | |_) | | (_) | | |    | |_ 
            |_|     |_|     \___/   \__,_|  \__,_|  \___|  \__| |_|  \___/  |_| |_|   |_| \_\  \___| | .__/   \___/  |_|     \__|
                                                                                                    |_|                         
                
'''    
def receipt_from_production_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ProductionReceiptItem.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'production/receipt_from_production_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'production/receipt_from_production_between_date.html', {'form': form})


def department_summary_by_dates(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department based on the given order number and dates
                quantity_by_department = ProductionReceiptItem.objects.filter(
                   created__range=(start_date, end_date)
                ).values('department').annotate(total_quantity=Sum('quantity'))
                
                return render(request, 'production/department_summary_by_dates.html', {'quantity_by_department': quantity_by_department})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'production/department_summary_by_dates.html', {'form': form})

def department_summary_by_month(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department and month
                quantity_by_department_monthly = ProductionReceiptItem.objects.filter(
                   created__range=(start_date, end_date)
                ).annotate(month=ExtractMonth('created')).values('month', 'department').annotate(total_quantity=Sum('quantity'))
                
                # Create a mapping of month numbers to month names
                month_names = {
                    1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
                }
                
                # Convert the month numbers to month names in the result
                for entry in quantity_by_department_monthly:
                    entry['month'] = month_names.get(entry['month'], 'Unknown Month')
                
                return render(request, 'production/department_summary_by_month.html', {'quantity_by_department_monthly': quantity_by_department_monthly})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'production/department_summary_by_month.html', {'form': form})






def receipt_from_production_based_on_order_no(request):
    form = OrderFilterForm(request.POST)  # Initialize form whether it's a POST or GET request
    
    if request.method == 'POST' and form.is_valid():
        order_no = form.cleaned_data['orderNo']
        
        # Retrieve ProductionReceiptItems based on the salesOrder
        receipt_items = ProductionReceiptItem.objects.filter(salesOrder=order_no)
        
        return render(request, 'production/receipt_from_production_based_on_order_no.html', {'form': form, 'items': receipt_items})
    
    return render(request, 'production/receipt_from_production_based_on_order_no.html', {'form': form})


def total_quantity_by_department(request):
    form = OrderFilterForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order_no = form.cleaned_data['orderNo']

        # Retrieve total quantity grouped by department based on the salesOrder
        quantity_by_department = ProductionReceiptItem.objects.filter(salesOrder=order_no).values('department').annotate(total_quantity=Sum('quantity'))

        return render(request, 'production/total_quantity_by_department.html', {'form': form, 'quantity_by_department': quantity_by_department})

    return render(request, 'production/total_quantity_by_department.html', {'form': form})


def receipt_from_production_monthly_data_view(request):
    year = None
    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = YearFilterForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ProductionReceiptItem.objects.filter(
                created__year=year
            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ProductionReceiptItem.objects.filter(
                created__year=year
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = YearFilterForm()

    return render(request, 'production/receipt_from_production_monthly_data_view.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form,
    })
    
    
    
def receipt_from_production_monthly_data_by_department_view(request):
    year = None
    department = None

    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = DepartmentYearFilter(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            department = form.cleaned_data['department'].id
            
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ProductionReceiptItem.objects.filter(
                created__year=year,
                department=department  

            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ProductionReceiptItem.objects.filter(
                created__year=year,
                department=department 
                
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = DepartmentYearFilter()

    return render(request, 'production/receipt_from_production_monthly_data_by_department_view.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form,
    
    })    
    
    
    






