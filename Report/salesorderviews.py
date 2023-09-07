from django.shortcuts import render
from django.db.models import Sum,Count
from Sales.models import SalesOrderInfo

#কাস্টমার অর্ডার সামারি রিপোর্ট 
def customer_summary(request):
    customer_summary_data = SalesOrderInfo.objects.values('customerName__name').annotate(
        total_amount=Sum('totalAmount'),
        total_qty=Sum('totalQty'),
        total_doc_no=Count('docNo')
    )
    
    return render(request, 'sales/customer_summary.html', {'customer_summary_data': customer_summary_data})



