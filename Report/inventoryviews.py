from django.shortcuts import render
from .forms import SalesEmployeeForm
from django.db.models import Sum
from ItemMasterData.models import Item,ItemReceiptinfo,ItemReceipt,ItemDeliveryinfo,ItemDelivery,Stock
from .forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter

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
                department=department.id
            )    
    
            return render(request, 'inventory/item_receipt_between_date_by_department.html', {'items': items})
    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_receipt_between_date_by_department.html', {'form': form})


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
                department=department.id
            )    
    
            return render(request, 'inventory/item_delivery_between_date_by_department.html', {'items': items})
    else:
        form = DateDepartmentFilter()

    return render(request, 'inventory/item_delivery_between_date_by_department.html', {'form': form})


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