from django.shortcuts import render
from django.db import models
from Sales.models import SalesOrderInfo,SalesOrderItem,DeliveryInfo,DeliveryItem
from BusinessPartners.models import BusinessPartner
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

