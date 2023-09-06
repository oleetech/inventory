from django.shortcuts import render
from .forms import SalesEmployeeForm
from django.db.models import Sum
from Sales.models import SalesEmployee,SalesOrderInfo,DeliveryInfo



# views.py


def sales_employee_data(request):
    total_order_amount = 0
    total_delivery_amount = 0
    balance_amount = 0

    if request.method == 'POST':
        form = SalesEmployeeForm(request.POST)
        if form.is_valid():
            selected_sales_employee = form.cleaned_data['sales_employee']
            
            # Calculate total_order_amount
            total_order_amount = SalesOrderInfo.objects.filter(sales_employee=selected_sales_employee).aggregate(total_amount=Sum('totalAmount'))['total_amount'] or 0
            
            # Calculate total_delivery_amount
            total_delivery_amount = DeliveryInfo.objects.filter(sales_employee=selected_sales_employee).aggregate(total_amount=Sum('totalAmount'))['total_amount'] or 0
            
            # Calculate balance_amount
            balance_amount = total_order_amount - total_delivery_amount
            
            return render(request, 'salesEmployee/sales_employee_data.html', {
                'selected_sales_employee': selected_sales_employee,
                'total_order_amount': total_order_amount,
                'total_delivery_amount': total_delivery_amount,
                'balance_amount': balance_amount,
            })
    else:
        form = SalesEmployeeForm()

    return render(request, 'salesEmployee/sales_employee_data.html', {'form': form})


def all_sales_employee_data(request):
    sales_employees = SalesEmployee.objects.all()

    # Calculate total_order_amount, total_delivery_amount, and balance_amount for each SalesEmployee
    for sales_employee in sales_employees:
        sales_employee.total_order_amount = SalesOrderInfo.objects.filter(sales_employee=sales_employee).aggregate(total_amount=Sum('totalAmount'))['total_amount'] or 0
        sales_employee.total_delivery_amount = DeliveryInfo.objects.filter(sales_employee=sales_employee).aggregate(total_amount=Sum('totalAmount'))['total_amount'] or 0
        sales_employee.balance_amount = sales_employee.total_order_amount - sales_employee.total_delivery_amount

    return render(request, 'salesEmployee/all_sales_employee_data.html', {'sales_employees': sales_employees})