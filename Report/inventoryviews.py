from django.shortcuts import render
from .forms import SalesEmployeeForm
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth
from django.db.models import IntegerField
from datetime import datetime
import calendar
from Production.models import ProductionComponent
from django.db import models

from ItemMasterData.models import Item,ItemReceiptinfo,ItemReceipt,ItemDeliveryinfo,ItemDelivery,Stock,IssueForProductionItem
from .forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter,ItemNameForm

'''
  ___   _                        ____                         _           _   
 |_ _| | |_    ___   _ __ ___   |  _ \    ___    ___    ___  (_)  _ __   | |_ 
  | |  | __|  / _ \ | '_ ` _ \  | |_) |  / _ \  / __|  / _ \ | | | '_ \  | __|
  | |  | |_  |  __/ | | | | | | |  _ <  |  __/ | (__  |  __/ | | | |_) | | |_ 
 |___|  \__|  \___| |_| |_| |_| |_| \_\  \___|  \___|  \___| |_| | .__/   \__|
                                                                 |_|          

'''
#ডেট অনুযায়ী আইটেম রিসিভ রিপোর্ট 
def item_receipt_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ItemReceipt.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'inventory/item_receipt_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_receipt_between_date.html', {'form': form})




#ডেট অনুযায়ী আইটেম ডেলিভারি রিপোর্ট 
def item_delivery_between_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                items_within_range = ItemDelivery.objects.filter(created__range=(start_date, end_date))
                
                return render(request, 'inventory/item_delivery_between_date.html', {'items': items_within_range})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_delivery_between_date.html', {'form': form})

#ডেট অনুযায়ী আইটেম রিসিভ রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে 
def item_receipt_between_date_by_department(request):
    form = DateDepartmentFilter(request.POST)
    if request.method == 'POST' and form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']
                        
            # Filter data based on form input
            items = ItemReceipt.objects.filter(
                created__range=(start_date, end_date),
                department=department.name
            )    
    
            return render(request, 'inventory/item_receipt_between_date_by_department.html', {'items': items})
    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_receipt_between_date_by_department.html', {'form': form})


#ডেট অনুযায়ী আইটেম ডেলিভারি রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে 
def item_delivery_between_date_by_department(request):
    form = DateDepartmentFilter(request.POST)
    if request.method == 'POST' and form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']
                        
            # Filter data based on form input
            items = ItemDelivery.objects.filter(
                created__range=(start_date, end_date),
                department=department.name
            )    
    
            return render(request, 'inventory/item_delivery_between_date_by_department.html', {'items': items})
    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_delivery_between_date_by_department.html', {'form': form})


#ডেট অনুযায়ী ডিপার্টমেন্ট আইটেম রিসিভ টোটাল সামারি  রিপোর্ট
def item_receipt_department_summary_by_dates(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department based on the given order number and dates
                quantity_by_department = ItemReceipt.objects.filter(
                   created__range=(start_date, end_date)
                ).values('department').annotate(total_quantity=Sum('quantity'))
                
                return render(request, 'inventory/item_receipt_department_summary_by_dates.html', {'quantity_by_department': quantity_by_department})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_receipt_department_summary_by_dates.html', {'form': form})


#ডেট অনুযায়ী ডিপার্টমেন্ট আইটেম ডেলিভারি টোটাল সামারি  রিপোর্ট
def item_delivery_department_summary_by_dates(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department based on the given order number and dates
                quantity_by_department = ItemDelivery.objects.filter(
                   created__range=(start_date, end_date)
                ).values('department').annotate(total_quantity=Sum('quantity'))
                
                return render(request, 'inventory/item_delivery_department_summary_by_dates.html', {'quantity_by_department': quantity_by_department})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_delivery_department_summary_by_dates.html', {'form': form})





# ১ বছরের মাস অনুযায়ী রিপোর্ট আইটেম রিসিভ 
def item_receipt_monthly_data(request):
    year = None
    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = YearFilterForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ItemReceipt.objects.filter(
                created__year=year
            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ItemReceipt.objects.filter(
                created__year=year
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = YearFilterForm()

    return render(request, 'inventory/item_receipt_monthly_data.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form,
    })
    
# ১ বছরের মাস অনুযায়ী রিপোর্ট আইটেম ডেলিভারি 
def item_delivery_monthly_data(request):
    year = None
    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = YearFilterForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ItemDelivery.objects.filter(
                created__year=year
            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ItemDelivery.objects.filter(
                created__year=year
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = YearFilterForm()

    return render(request, 'inventory/item_delivery_monthly_data.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form,
    })  
    
    
# ১ বছরের মাস অনুযায়ী রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে আইটেম রিসিভ    
def item_receipt_monthly_data_by_department(request):
    year = None
    department = None

    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = DepartmentYearFilter(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            department = form.cleaned_data['department']
            
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ItemReceipt.objects.filter(
                created__year=year,
                department=department  

            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ItemReceipt.objects.filter(
                created__year=year,
                department=department.name 
                
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = DepartmentYearFilter()

    return render(request, 'inventory/item_receipt_monthly_data_by_department.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form
    
    })         
    
    
# ১ বছরের মাস অনুযায়ী রিপোর্ট ডিপার্টমেন্ট সিলেক্ট করে আইটেম ডেলিভারি    
def item_delivery_monthly_data_by_department(request):
    year = None
    department = None

    total_quantity = 0
    monthly_totals_dict = {i: 0 for i in range(1, 13)}

    if request.method == 'POST':
        form = DepartmentYearFilter(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            department = form.cleaned_data['department']
            
            # Calculate the 12-month total quantity for the selected year
            total_quantity = ItemDelivery.objects.filter(
                created__year=year,
                department=department  

            ).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

            # Calculate monthly totals for the selected year
            monthly_totals = ItemDelivery.objects.filter(
                created__year=year,
                department=department.name 
                
            ).values('created__month').annotate(monthly_qty=Sum('quantity'))

            # Populate the dictionary with the monthly totals
            for entry in monthly_totals:
                month = entry['created__month']
                qty = entry['monthly_qty']
                monthly_totals_dict[month] = qty
    else:
        form = DepartmentYearFilter()

    return render(request, 'inventory/item_delivery_monthly_data_by_department.html', {
        'year': year,
        'total_quantity': total_quantity,
        'monthly_totals_dict': monthly_totals_dict,
        'form': form
    
    })     
    
    
# ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল আইটেম রিসিভ ডেট সিলেক্ট করে  
def item_receipt_department_summary_by_month_based_on_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department and month
                quantity_by_department_monthly = ItemReceipt.objects.filter(
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
                
                return render(request, 'inventory/item_receipt_department_summary_by_month_based_on_date.html', {'quantity_by_department_monthly': quantity_by_department_monthly})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_receipt_department_summary_by_month_based_on_date.html', {'form': form})           


# ১২ মাস আকারে প্রতিটি ডিপার্টমেন্ট টোটাল আইটেম ডেলিভারি ডেট সিলেক্ট করে  
def item_delivery_department_summary_by_month_based_on_date(request):
    form = DateFilterForm(request.POST)
    
    if request.method == 'POST' and form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        
        if start_date and end_date:
            try:
                # Retrieve total quantity grouped by department and month
                quantity_by_department_monthly = ItemDelivery.objects.filter(
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
                
                return render(request, 'inventory/item_delivery_department_summary_by_month_based_on_date.html', {'quantity_by_department_monthly': quantity_by_department_monthly})
            except ValueError:
                # Handle invalid date format
                pass
    
    return render(request, 'inventory/item_delivery_department_summary_by_month_based_on_date.html', {'form': form})    
 

#ডেট অনুযায়ী প্রোডাক্ট সামারি আইটেম রিসিভ
def item_receipt_total_by_name_between_dates(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the database to get the total grouped by ProductionReceiptItem.name
            totals = ItemReceipt.objects.filter(
                created__gte=start_date,
                created__lte=end_date
            ).values('name').annotate(total_quantity=Sum('quantity'))

            return render(request, 'inventory/item_receipt_total_by_name_between_dates.html', {'totals': totals})

    else:
        form = DateFilterForm()

    return render(request, 'inventory/item_receipt_total_by_name_between_dates.html', {'form': form}) 


#ডেট অনুযায়ী প্রোডাক্ট সামারি আইটেম ডেলিভারি
def item_delivery_total_by_name_between_dates(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query the database to get the total grouped by ProductionReceiptItem.name
            totals = ItemDelivery.objects.filter(
                created__gte=start_date,
                created__lte=end_date
            ).values('name').annotate(total_quantity=Sum('quantity'))

            return render(request, 'inventory/item_delivery_total_by_name_between_dates.html', {'totals': totals})

    else:
        form = DateFilterForm()

    return render(request, 'inventory/item_delivery_total_by_name_between_dates.html', {'form': form}) 



#ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে আইটেম রিসিভ
def item_receipt_total_by_name_between_dates_and_department(request):
    if request.method == 'POST':
        form = DateDepartmentFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']

            # Query the database to get the total grouped by ProductionReceiptItem.name
            totals = ItemReceipt.objects.filter(
                created__gte=start_date,
                created__lte=end_date,
                department=department.name
                
            ).values('name').annotate(total_quantity=Sum('quantity'))

            return render(request, 'inventory/item_receipt_total_by_name_between_dates_and_department.html', {'totals': totals})

    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_receipt_total_by_name_between_dates_and_department.html', {'form': form})


#ডেট অনুযায়ী প্রোডাক্ট সামারি ডিপার্টমেন্ট সিলেক্ট করে আইটেম ডেলিভারি
def item_delivery_total_by_name_between_dates_and_department(request):
    if request.method == 'POST':
        form = DateDepartmentFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']

            # Query the database to get the total grouped by ProductionReceiptItem.name
            totals = ItemDelivery.objects.filter(
                created__gte=start_date,
                created__lte=end_date,
                department=department.name
                
            ).values('name').annotate(total_quantity=Sum('quantity'))

            return render(request, 'inventory/item_delivery_total_by_name_between_dates_and_department.html', {'totals': totals})

    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_delivery_total_by_name_between_dates_and_department.html', {'form': form})


# নির্দিষ্ট আইটেমের ডেট অনুযায়ী রিপোর্ট আইটেম রিসিভ 
def item_receipt_between_date_by_name(request):
    item_receipts = None

    if request.method == 'POST':
        form = ItemNameForm(request.POST)
        if form.is_valid():
            selected_item = form.cleaned_data['item_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Filter ItemReceipt objects based on the selected item and date range
            item_receipts = ItemReceipt.objects.filter(created__range=(start_date, end_date))
            
            if selected_item:
                item_receipts = item_receipts.filter(name=selected_item.name)

    else:
        form = ItemNameForm()

    return render(request, 'inventory/item_receipt_between_date_by_name.html', {'form': form, 'item_receipts': item_receipts})


# নির্দিষ্ট আইটেমের ডেট অনুযায়ী রিপোর্ট আইটেম ডেলিভারি 
def item_delivery_between_date_by_name(request):
    item_receipts = None

    if request.method == 'POST':
        form = ItemNameForm(request.POST)
        if form.is_valid():
            selected_item = form.cleaned_data['item_name']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Filter ItemReceipt objects based on the selected item and date range
            item_receipts = ItemDelivery.objects.filter(created__range=(start_date, end_date))
            
            if selected_item:
                item_receipts = item_receipts.filter(name=selected_item.name)

    else:
        form = ItemNameForm()

    return render(request, 'inventory/item_delivery_between_date_by_name.html', {'form': form, 'item_receipts': item_receipts})


def issue_for_production_balance_report(request):
    balance_report_data = None
    form = OrderFilterForm()  # Initialize the form without any request data
    
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            doc_no = form.cleaned_data['orderNo']

            # Get all ProductionComponents for the specified docNo
            production_components = ProductionComponent.objects.filter(docNo=doc_no)

            # Initialize a dictionary to store the quantities for each code
            code_quantities = {}

            # Calculate ProductionComponent quantities
            for pc in production_components:
                code = pc.code
                quantity = pc.quantity
                name = pc.name

                if code not in code_quantities:
                    code_quantities[code] = {'production_quantity': 0, 'issue_quantity': 0, 'name': name}

                code_quantities[code]['production_quantity'] += quantity

            # Calculate IssueForProductionItem quantities based on productionNo
            issue_items = IssueForProductionItem.objects.filter(productionNo=doc_no)
            for issue_item in issue_items:
                code = issue_item.code
                name = issue_item.name  # Update the name for each item

                quantity = issue_item.quantity

                if code not in code_quantities:
                    code_quantities[code] = {'production_quantity': 0, 'issue_quantity': 0, 'name': name}

                code_quantities[code]['issue_quantity'] += quantity

            # Calculate balance for each code
            balance_report_data = []
            for code, quantities in code_quantities.items():
                production_quantity = quantities['production_quantity']
                issue_quantity = quantities['issue_quantity']
                name = quantities['name']  # Get the name from the dictionary
                balance = production_quantity - issue_quantity

                balance_report_data.append({
                    'code': code,
                    'name': name,
                    'production_quantity': production_quantity,
                    'issue_quantity': issue_quantity,
                    'balance': balance,
                })

    return render(request, 'inventory/issue_for_production_balance_report.html', {'form': form, 'balance_report_data': balance_report_data})
