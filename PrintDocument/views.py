from django.shortcuts import render
from django.http import HttpResponse
from Report.forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter
from django.shortcuts import render, get_object_or_404
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryInfo,DeliveryItem
from GeneralSettings.models import Company
# Create your views here.
def home(request):
    return render(request, 'PrintDocument/index.html')

def salesOrder(request):
    company = Company.objects.first()
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']

            # Retrieve SalesOrderInfo and SalesOrderItem data based on order_no
            sales_order_info = get_object_or_404(SalesOrderInfo, docNo=order_no)
            sales_order_items = SalesOrderItem.objects.filter(docNo=order_no)

            return render(request, 'PrintDocument/salesOrder.html', {
                'sales_order_info': sales_order_info,
                'sales_order_items': sales_order_items,
                'company':company
            })
    else:
        form = OrderFilterForm()

    return render(request, 'PrintDocument/salesOrder.html', {'form': form})


def delivery(request):
    company = Company.objects.first()
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']

            # Retrieve SalesOrderInfo and SalesOrderItem data based on order_no
            delivery_info = get_object_or_404(DeliveryInfo, docNo=order_no)
            delivery_items = DeliveryItem.objects.filter(docNo=order_no)

            return render(request, 'PrintDocument/delivery.html', {
                'delivery_info': delivery_info,
                'delivery_items': delivery_items,
                'company':company
            })
    else:
        form = OrderFilterForm()

    return render(request, 'PrintDocument/delivery.html', {'form': form})
