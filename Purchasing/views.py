from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PurchaseOrderInfo,GoodsReceiptPoInfo,PurchaseItem
# Create your views here.
@csrf_exempt
def purchaseorderinfo(request):
    if request.method == 'POST':
        purchaseOrder  = request.POST.get('purchaseOrder')
        

        # Replace the filter conditions with the ones you need
        try:
            orderinfo = PurchaseOrderInfo.objects.get(docNo=purchaseOrder)
            response_data = {
                
                'docNo': purchaseOrder,
                'customerName': orderinfo.customerName.id,
                'address':orderinfo.address,
                'totalAmount':orderinfo.totalAmount,
                'totalQty':orderinfo.totalQty                

                
            }
            return JsonResponse(response_data)
        except PurchaseOrderInfo.DoesNotExist:
            return JsonResponse({'error': 'No data found for the given orderno and orderlineNo'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def goodsreceiptpoline(request):
    if request.method == 'POST':
        receiptNo = int(request.POST.get('receiptNo'))
        lineNo = int(request.POST.get('lineNo'))

        try:
            receipt_item = PurchaseItem.objects.get(docNo=receiptNo, lineNo=lineNo)

            response_data = {
                'receiptNumber': receipt_item.docNo,
                'code': receipt_item.code,
                'name': receipt_item.name,
                'quantity': receipt_item.quantity,
                'uom': receipt_item.uom,                
                'price': receipt_item.price,
                'priceTotal': receipt_item.priceTotal,             
             
                # Include other fields you want to retrieve
            }
            return JsonResponse(response_data)
        except PurchaseItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})
