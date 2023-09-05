from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Production.models import ProductionReceiptItem

@csrf_exempt
def ajax_view(request):
    if request.method == 'POST':
        receiptNo = int(request.POST.get('receiptNo'))
        lineNo = int(request.POST.get('lineNo'))

        try:
            receipt_item = ProductionReceiptItem.objects.get(receiptNumber_id=receiptNo, lineNo=lineNo)

            response_data = {
                'receiptNumber': receipt_item.receiptNumber_id,
                'salesOrder': receipt_item.salesOrder,
                'code': receipt_item.code,
                'name': receipt_item.name,
                'quantity': receipt_item.quantity,
                'price': receipt_item.price,
                'priceTotal': receipt_item.priceTotal,
                # Include other fields you want to retrieve
            }
            return JsonResponse(response_data)
        except ProductionReceiptItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})


from .models import SalesOrderItem
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def get_sales_order_info(request):
    if request.method == 'POST':
        docNo = request.POST.get('docNo')
        print("Received docNo:", docNo)  # Add this line for debugging
        try:
            order_items = SalesOrderItem.objects.filter(docNo=docNo)

            if order_items.exists():  # Check if there are any results
                # Assuming you want to return a list of 'name' values for all matching rows
                response_data = {
                    'code': [item.code for item in order_items],
                    'names': [item.name for item in order_items]
                }
            else:
                # Handle the case where no matching rows were found
                response_data = {
                    'message': 'No matching items found.'
                }
            print("Response data:", response_data)  # Add this line for debugging
            return JsonResponse(response_data)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Sales order not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

