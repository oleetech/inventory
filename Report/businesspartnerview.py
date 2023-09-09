from django.shortcuts import render
from django.db import models
from django.db.models import Sum
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryInfo,DeliveryItem
from BusinessPartners.models import BusinessPartner
from Purchasing.models import PurchaseOrderInfo
from .forms import CustomerNameForm

#কাস্টমার অনুযায়ী সেলস অর্ডার লিস্ট 
def sales_order_based_on_customer_name (request):
    sales_orders = []  # To store SalesOrderInfo objects

    if request.method == 'POST':
        form = CustomerNameForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data['customerName']

            # Query SalesOrderInfo objects based on the selected customerName
            sales_orders = SalesOrderInfo.objects.filter(customerName=customer_name)
    else:
        form = CustomerNameForm()

    return render(request, 'businesspartner/sales_order_based_on_customer_name.html', {'form': form, 'sales_orders': sales_orders})
 #সকল কাস্টমারের সেলস ডেলিভারি রিপোর্ট 
def customer_sales_report(request):
    # Query the SalesOrderInfo and SalesOrderItem models to retrieve sales data
    sales_data = SalesOrderInfo.objects.values(
        'customerName__name'  # Assuming 'name' is the field representing the customer's name in the BusinessPartner model
    ).annotate(
        total_sales_amount=Sum('totalAmount'),
        total_sales_quantity=Sum('totalQty')
    ).order_by('customerName')

    return render(request, 'businesspartner/customer_sales_report.html', {'sales_data': sales_data})