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