from django.shortcuts import render
from django.db import models
from django.db.models import Sum,Count
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryItem
from Production.models import ProductionReceiptItem
from datetime import datetime, timedelta
from .forms import AgeFilterForm,SalesOrderStatusFilterForm,OrderFilterForm
#কাস্টমার অর্ডার সামারি রিপোর্ট 
def customer_summary(request):
    customer_summary_data = SalesOrderInfo.objects.values('customerName__name').annotate(
        total_amount=Sum('totalAmount'),
        total_qty=Sum('totalQty'),
        total_doc_no=Count('docNo')
    )
    
    return render(request, 'sales/customer_summary.html', {'customer_summary_data': customer_summary_data})


#সেলস অর্ডার এর বয়স দেখা     
def sales_order_aging_report(request):
    today = datetime.now().date()

    age_ranges = {
        '0-30 Days': (0, 30),
        '31-60 Days': (31, 60),
        '61-90 Days': (61, 90),
        'Over 90 Days': (91, None),
    }

    aging_data = {range_name: 0 for range_name in age_ranges}

    for range_name, (start_days, end_days) in age_ranges.items():
        if end_days is None:
            sales_orders = SalesOrderInfo.objects.filter(
                created__lte=today - timedelta(days=start_days)
            )
        else:
            sales_orders = SalesOrderInfo.objects.filter(
                created__range=(
                    today - timedelta(days=end_days),
                    today - timedelta(days=start_days - 1)
                ),
                status='O'
            )

        aging_data[range_name] = sales_orders.count()

    return render(request, 'sales/sales_order_aging_report.html', {'aging_data': aging_data})

#বয়স অনুযায়ী  সেলস অর্ডার দেখা 
def filter_orders_by_age(request):
    if request.method == 'POST':
        form = AgeFilterForm(request.POST)
        if form.is_valid():
            age_in_days = form.cleaned_data['age_in_days']
            today = datetime.now().date()
            start_date = today - timedelta(days=age_in_days)

            filtered_orders = SalesOrderInfo.objects.filter(
                created__gte=start_date,status='O'
            )
            order_numbers = filtered_orders.values_list('docNo','customerName__name')

            return render(request, 'sales/filter_orders_by_age.html', {'order_numbers': filtered_orders})
    else:
        form = AgeFilterForm()

    return render(request, 'sales/filter_orders_by_age.html', {'form': form})

#স্ট্যাটাস অনুযায়ী  সেলস অর্ডার দেখা 
def sales_order_status_filter(request):
    if request.method == 'POST':
        form = SalesOrderStatusFilterForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status:
                filtered_orders = SalesOrderInfo.objects.filter(status=status)
            else:
                filtered_orders = SalesOrderInfo.objects.all()
        else:
            filtered_orders = SalesOrderInfo.objects.all()
    else:
        form = SalesOrderStatusFilterForm()
        filtered_orders = SalesOrderInfo.objects.all()

    return render(request, 'sales/sales_order_status_filter.html', {'form': form, 'filtered_orders': filtered_orders})
#প্রোডাক্ট অনুযায়ী  সেলস অর্ডার 
def sales_order_by_product_report(request):
    # Retrieve sales order data grouped by product name
    product_data = (
        SalesOrderItem.objects.values('name')
        .annotate(total_quantity=models.Sum('quantity'))
        .annotate(total_amount=models.Sum(models.F('price') * models.F('quantity'), output_field=models.DecimalField()))
        .order_by('name')
    )

    return render(request, 'sales/sales_order_by_product_report.html', {'product_data': product_data})



def calculate_production_balance(order_no):
    sales_orders = SalesOrderItem.objects.filter(docNo=order_no)
    balance_data = []
    
    for sales_order in sales_orders:
        order_line_no = sales_order.lineNo
        sales_order_quantity = sales_order.quantity
        receipt_quantity_sum = ProductionReceiptItem.objects.filter(orderlineNo=order_line_no).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if receipt_quantity_sum is None:
            receipt_quantity_sum = 0
        balance = sales_order_quantity - receipt_quantity_sum
        balance_data.append({
            'order_line_no': order_line_no,
            'name': sales_order.name,
            'docNo': sales_order.docNo,
            'quantity': sales_order.quantity,
            'receipt_quantity_sum': receipt_quantity_sum,
            'balance': balance,
        })
    
    return balance_data



def production_balance_line_wise(request):
    order_no = None
    balance_data = []

    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']
            balance_data = calculate_production_balance(order_no)
    
    else:
        form = OrderFilterForm()
    
    return render(request, 'sales/production_balance_line_wise.html', {'order_no': order_no, 'balance_data': balance_data, 'form': form})



def calculate_order_balance(order_no):
    sales_orders = SalesOrderItem.objects.filter(docNo=order_no)
    balance_data = []

    for sales_order in sales_orders:
        order_line_no = sales_order.lineNo
        sales_order_quantity = sales_order.quantity
        receipt_quantity_sum = ProductionReceiptItem.objects.filter(orderlineNo=order_line_no).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if receipt_quantity_sum is None:
            receipt_quantity_sum = 0
        production_receipt_balance = sales_order_quantity - receipt_quantity_sum

        delivery_quantity_sum = DeliveryItem.objects.filter(orderNo=order_no, orderlineNo=order_line_no).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if delivery_quantity_sum is None:
            delivery_quantity_sum = 0
        delivery_balance = delivery_quantity_sum

        balance_data.append({
            'order_line_no': order_line_no,
            'name': sales_order.name,
            'docNo': sales_order.docNo,
            'quantity': sales_order.quantity,
            'receipt_quantity_sum': receipt_quantity_sum,
            'production_receipt_balance': production_receipt_balance,
            'delivery_quantity_sum': delivery_quantity_sum,
            'delivery_balance': delivery_balance,
        })

    return balance_data


def order_balance_production_delivery_line_wise(request):
    order_no = None
    balance_data = {}

    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']
            balance_data = calculate_order_balance(order_no)
    
    else:
        form = OrderFilterForm()
    
    return render(request, 'sales/order_balance_production_delivery_line_wise.html', {'order_no': order_no, 'balance_data': balance_data, 'form': form})