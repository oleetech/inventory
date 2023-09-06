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

