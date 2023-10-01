from django.shortcuts import render
from django.http import HttpResponse
from Report.forms import DateFilterForm,OrderFilterForm,YearFilterForm,DepartmentYearFilter,DateDepartmentFilter,OrderDepartmentFilter
from django.shortcuts import render, get_object_or_404
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryInfo,DeliveryItem,SalesQuotetionInfo,SalesQuotetionItem
from Production.models import Production,ProductionComponent,ProductionReceipt,ProductionReceiptItem,BillOfMaterials,ChildComponent
from GeneralSettings.models import Company
# Create your views here.
def home(request):
    return render(request, 'PrintDocument/index.html')


def salesQuotetion(request):
    company = Company.objects.first()
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']

            
            sales_order_info = get_object_or_404(SalesQuotetionInfo, docNo=order_no)
            sales_order_items = SalesQuotetionItem.objects.filter(order__docNo=order_no)

            return render(request, 'PrintDocument/salesQuotation.html', {
                'sales_order_info': sales_order_info,
                'sales_order_items': sales_order_items,
                'company':company
            })
    else:
        form = OrderFilterForm()

    return render(request, 'PrintDocument/salesQuotation.html', {'form': form})


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

def production_order(request):
    company = Company.objects.first()
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']

            # Retrieve SalesOrderInfo and SalesOrderItem data based on order_no
            info = get_object_or_404(Production, docno=order_no)
            items = ProductionComponent.objects.filter(docNo=order_no)

            return render(request, 'PrintDocument/production_order.html', {
                'info': info,
                'items': items,
                'company':company
            })
    else:
        form = OrderFilterForm()

    return render(request, 'PrintDocument/production_order.html', {'form': form})

