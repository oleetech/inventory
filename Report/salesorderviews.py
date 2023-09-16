from django.shortcuts import render
from django.db import models
from django.db.models import Sum,Count,F,ExpressionWrapper, DecimalField
from collections import defaultdict
from decimal import Decimal
from ItemMasterData.models import Item,ItemGroup
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryItem,DeliveryInfo
from Production.models import ProductionReceiptItem
from datetime import datetime, timedelta
from .forms import AgeFilterForm,SalesOrderStatusFilterForm,OrderFilterForm,DateFilterForm,OrderDepartmentFilter,DateDepartmentFilter,ItemGroupForm
#কাস্টমার অর্ডার সামারি রিপোর্ট  Customer Wise Order Summary
def customer_summary(request):
    customer_summary_data = SalesOrderInfo.objects.values('customerName__name').annotate(
        total_amount=Sum('totalAmount'),
        total_qty=Sum('totalQty'),
        total_doc_no=Count('docNo')
    )
    
    return render(request, 'sales/customer_summary.html', {'customer_summary_data': customer_summary_data})


#সেলস অর্ডার এর বয়স দেখা     Sales Order Ageing Report
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

#বয়স অনুযায়ী  সেলস অর্ডার দেখা Age Wise Sales Order Report By Days
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

#অর্ডার Open Hold স্ট্যাটাস অনুযায়ী  সেলস অর্ডার দেখা  Sales Order Status Filter
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
#প্রোডাক্ট অনুযায়ী  সেলস অর্ডার Product Based Sales Order
def sales_order_by_product_report(request):
    # Retrieve sales order data grouped by product name
    product_data = (
        SalesOrderItem.objects.values('name')
        .annotate(total_quantity=models.Sum('quantity'))
        .annotate(total_amount=models.Sum(models.F('price') * models.F('quantity'), output_field=models.DecimalField()))
        .order_by('name')
    )

    return render(request, 'sales/sales_order_by_product_report.html', {'product_data': product_data})


#সাইজ অনুযায়ী প্রোডাকশন  ব্যালেন্স Size Wise Production Balance Report
def calculate_production_balance(order_no):
    sales_orders = SalesOrderItem.objects.filter(docNo=order_no)
    balance_data = []

    for sales_order in sales_orders:
        order_line_no = sales_order.lineNo
        sales_order_quantity = sales_order.quantity
        receipt_quantity_sum = ProductionReceiptItem.objects.filter(orderlineNo=order_line_no,salesOrder=sales_order.docNo).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if receipt_quantity_sum is None:
            receipt_quantity_sum = 0
        production_receipt_balance = sales_order_quantity - receipt_quantity_sum
        
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


#সাইজ অনুযায়ী প্রোডাকশন ও ডেলিভারি ব্যালেন্স  Size Wise Production And Delivery Balance
def calculate_order_balance(order_no):
    sales_orders = SalesOrderItem.objects.filter(docNo=order_no)
    balance_data = []

    for sales_order in sales_orders:
        order_line_no = sales_order.lineNo
        sales_order_quantity = sales_order.quantity
        receipt_quantity_sum = ProductionReceiptItem.objects.filter(orderlineNo=order_line_no,salesOrder=sales_order.docNo).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if receipt_quantity_sum is None:
            receipt_quantity_sum = 0
        production_receipt_balance = sales_order_quantity - receipt_quantity_sum

        delivery_quantity_sum = DeliveryItem.objects.filter(orderNo=sales_order.docNo, orderlineNo=order_line_no).aggregate(total_quantity=models.Sum('quantity'))['total_quantity']
        if delivery_quantity_sum is None:
            delivery_quantity_sum = 0
        delivery_balance = sales_order_quantity - delivery_quantity_sum
        ready_in_hand = receipt_quantity_sum - delivery_quantity_sum

        balance_data.append({
            'order_line_no': order_line_no,
            'name': sales_order.name,
            'docNo': sales_order.docNo,
            'size': sales_order.size,  
            'color': sales_order.color,                        
            'quantity': sales_order.quantity,
            'receipt_quantity_sum': receipt_quantity_sum,
            'production_receipt_balance': production_receipt_balance,
            'delivery_quantity_sum': delivery_quantity_sum,
            'delivery_balance': delivery_balance,
            'ready_in_hand':ready_in_hand,
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

# অর্ডার অনুযায়ী ডেলিভারি চালান বিস্তারিত Delivery Challan Based On Order No
def delivery_items_by_order(request):
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']
            delivery_items = DeliveryItem.objects.filter(orderNo=order_no)
            return render(request, 'sales/delivery_items_by_order.html', {'delivery_items': delivery_items})
    else:
        form = OrderFilterForm()

    return render(request, 'sales/delivery_items_by_order.html', {'form': form})


#অর্ডার আইটেম ব্যালেন্স ডিপার্টমেন্ট অনুযায়ী  Order Item Balance Department Wise  Pasha Sir
def balance_report_view(request):
   
    # Calculate the balance report using the method from your models
    balance_report = ProductionReceiptItem.get_balance_report()
    # Calculate the total sum of SalesOrderItem.quantity for each code
    sales_order_totals = SalesOrderItem.objects.values('code').annotate(
        sales_total=Sum('quantity')
    )    
    return render(request, 'sales/balance_report_view.html', {'balance_report': balance_report,'sales_order_totals': sales_order_totals})

#অর্ডার অনুযায়ী চালান লিস্ট Order Wise Challan List
def delivery_challan_list_based_on_order(request):
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['orderNo']

            # Query unique values of DeliveryItem.doc based on the provided order number
            unique_docs = DeliveryItem.objects.filter(orderNo=order_number).values('docNo').distinct()

            return render(request, 'sales/delivery_challan_list_based_on_order.html', {'unique_docs': unique_docs, 'order_number': order_number})
    else:
        form = OrderFilterForm()

    return render(request, 'sales/delivery_challan_list_based_on_order.html', {'form': form})



# পেন্ডিং পার্টিকুলার  অর্ডার অনুযায়ী  Pending Particular Based On Order No
def pending_particular_based_on_order_no(request):
    if request.method == 'POST':
        form = OrderDepartmentFilter(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']
            department = form.cleaned_data['department']

            # Get ProductionReceiptItem data based on salesOrder
            receipt_items = ProductionReceiptItem.objects.filter(salesOrder=order_no,department=department.name)

            # Extract docNo values from receipt_items queryset
            doc_no_values = receipt_items.values_list('docNo', flat=True)

            # Get DeliveryItem data for the docNo values
            delivery_items = DeliveryItem.objects.filter(receiptNo__in=doc_no_values)

            # Find missing lineNo entries in ProductionReceiptItem
            missing_items = []
            for receipt_item in receipt_items:
                if not delivery_items.filter(receiptNo=receipt_item.docNo, lineNo=receipt_item.lineNo).exists():
                    missing_items.append(receipt_item)

            return render(request, 'sales/pending_particular_based_on_order_no.html', {'missing_items': missing_items})

    else:
        form = OrderDepartmentFilter()

    return render(request, 'sales/pending_particular_based_on_order_no.html', {'form': form})




#পেন্ডিং পার্টিকুলার  ডেট অনুযায়ী Pending Particular Based On Date
def pending_particular_between_on_date(request):
    if request.method == 'POST':
        form = DateDepartmentFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']

            # Get ProductionReceiptItem data within the date range
            receipt_items = ProductionReceiptItem.objects.filter(created__range=[start_date, end_date],department=department.name)

            # Get DeliveryItem data for the same docNo values
            delivery_items = DeliveryItem.objects.filter(receiptNo__in=receipt_items.values_list('docNo', flat=True))

            # Find missing lineNo entries in ProductionReceiptItem
            missing_items = []
            for receipt_item in receipt_items:
                if not delivery_items.filter(receiptNo=receipt_item.docNo, lineNo=receipt_item.lineNo).exists():
                    missing_items.append(receipt_item)

            return render(request, 'sales/pending_particular_between_on_date.html', {'missing_items': missing_items})

    else:
        form = DateDepartmentFilter()

    return render(request, 'sales/pending_particular_between_on_date.html', {'form': form})




# Pending Particular Item Wise 
def sum_quantity_by_name(request):
    if request.method == 'POST':
        form = DateDepartmentFilter(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            department = form.cleaned_data['department']

            # Get ProductionReceiptItem data within the date range and filtered by department
            receipt_items = ProductionReceiptItem.objects.filter(
                created__range=[start_date, end_date],
                department=department.name
            )

            # Group by 'name' and calculate the sum of 'quantity' for each group
            sum_by_name = receipt_items.values('name').annotate(total_quantity=Sum('quantity'))

            # Get DeliveryItem data for the same docNo values
            delivery_items = DeliveryItem.objects.filter(receiptNo__in=receipt_items.values_list('docNo', flat=True))

            # Calculate the sum of missing DeliveryItem quantities for each 'name'
            missing_quantity_by_name = defaultdict(Decimal)  # Initialize as Decimal
            for receipt_item in receipt_items:
                if not delivery_items.filter(receiptNo=receipt_item.docNo, lineNo=receipt_item.lineNo).exists():
                    missing_quantity_by_name[receipt_item.name] += Decimal(receipt_item.quantity)

            # Convert the defaultdict to a regular dictionary for the template
            missing_quantity_by_name = dict(missing_quantity_by_name)

            return render(request, 'sales/sum_quantity_by_name.html', {
                'sum_by_name': sum_by_name,
                'missing_quantity_by_name': missing_quantity_by_name,
            })

    else:
        form = DateDepartmentFilter()

    return render(request, 'sales/sum_quantity_by_name.html', {'form': form})




#অর্ডার অনুযায়ী ডেলিভারি ও চালান রেসিভ দেখা Order Wise Delivery And Challan Received
def check_delivery_status(request):
    if request.method == 'POST':
        form = OrderFilterForm(request.POST)
        if form.is_valid():
            order_no = form.cleaned_data['orderNo']
            
            delivery_info_queryset = DeliveryInfo.objects.filter(salesOrder=order_no)
            return render(request, 'sales/delivery_status.html', {'delivery_info_queryset': delivery_info_queryset})
    else:
        form = OrderFilterForm()

    return render(request, 'sales/delivery_status.html', {'form': form})


#অর্ডার অনুযায়ী ডেলিভারি পার্সেন্টেজ  Order Wise Delivery Percentage
def calculate_delivery_percentage(request):
    # Query SalesOrderInfo to retrieve totalAmount and totalQty
    sales_orders = SalesOrderInfo.objects.all()

    # Calculate the sum of totalAmount and totalQty for each docNo
    delivery_totals = DeliveryInfo.objects.values('salesOrder').annotate(
        total_delivery_amount=Sum('totalAmount'),
        total_delivery_qty=Sum('totalQty')
    )

    # Calculate percentage and add it to the SalesOrderInfo objects
    for sales_order in sales_orders:
        matching_delivery_info = next(
            (item for item in delivery_totals if item['salesOrder'] == sales_order.docNo),
            None
        )
        if matching_delivery_info:
            delivery_total_amount = matching_delivery_info['total_delivery_amount']
            delivery_total_qty = matching_delivery_info['total_delivery_qty']
            total_amount = sales_order.totalAmount
            total_qty = sales_order.totalQty
            if total_amount:
                percentage_amount = (delivery_total_amount / total_amount) * 100
                percentage_qty = (delivery_total_qty / total_qty) * 100
                # Add these calculated values to the sales_order object
                sales_order.delivery_total_amount = delivery_total_amount
                sales_order.delivery_total_qty = delivery_total_qty
                sales_order.delivery_percentage_amount = percentage_amount
                sales_order.delivery_percentage_qty = percentage_qty
            else:
                # Handle cases where total_amount is zero or None
                sales_order.delivery_total_amount = 0
                sales_order.delivery_total_qty = 0
                sales_order.delivery_percentage_amount = None
                sales_order.delivery_percentage_qty = None
        else:
            # Handle cases where there is no matching delivery info
            sales_order.delivery_total_amount = 0
            sales_order.delivery_total_qty = 0
            sales_order.delivery_percentage_amount = None
            sales_order.delivery_percentage_qty = None

    return render(request, 'sales/calculate_delivery_percentage.html', {'sales_orders': sales_orders})

# আইটেম group সিলেক্ট করে আইটেম group  অনুযায়ী টোটাল সেলস quantity এবং  এমাউন্ট  Total Sales Select By Item Group
def calculate_summary(request):
    if request.method == 'POST':
        form = ItemGroupForm(request.POST)
        if form.is_valid():
            selected_item_group = form.cleaned_data['item_group']
            
            # Get a list of Item objects belonging to the selected ItemGroup
            items_in_group = Item.objects.filter(item_group=selected_item_group)
            
            # Get the codes of the items in the selected ItemGroup
            item_codes = [item.code for item in items_in_group]
            
            # Calculate sum of quantity and priceTotal for SalesOrderItem
            summary_data = SalesOrderItem.objects.filter(
                code__in=item_codes  # Match SalesOrderItem.code with Item.code
            ).aggregate(
                total_quantity=Sum('quantity'),
                total_price_total=Sum('priceTotal')
            )
            
            return render(request, 'sales/item_group_sales_summary.html', {
                'selected_item_group': selected_item_group,
                'total_quantity': summary_data['total_quantity'],
                'total_price_total': summary_data['total_price_total'],
            })
    else:
        form = ItemGroupForm()

    return render(request, 'sales/item_group_sales_summary.html', {'form': form})

#আইটেম অনুযায়ী অর্ডার টোটাল আইটেম quantity, এমাউন্ট সামারি  Item Based Order Total Quantity And Amount
def sales_order_item_wise_summary(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Get the total quantity and total amount for each code, filtered by date range
            summary_data = SalesOrderItem.objects.filter(created__gte=start_date, created__lte=end_date).values('created', 'code', 'name').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum('priceTotal')
            ).order_by('created')
            
            return render(request, 'sales/sales_order_item_wise_summary.html', {'summary_data': summary_data, 'form': form})
    else:
        form = DateFilterForm()
        summary_data = []  # Empty data for initial display
    
    return render(request, 'sales/sales_order_item_wise_summary.html', {'form': form})

