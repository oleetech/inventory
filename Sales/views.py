from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpRequest
from django.views.decorators.csrf import csrf_exempt
from Production.models import ProductionReceiptItem

@csrf_exempt
def ajax_view(request):
    if request.method == 'POST':
        receiptNo = int(request.POST.get('receiptNo'))
        lineNo = int(request.POST.get('lineNo'))

        try:
            receipt_item = ProductionReceiptItem.objects.get(docNo=receiptNo, lineNo=lineNo)

            response_data = {
                'receiptNumber': receipt_item.docNo,
                'salesOrder': receipt_item.salesOrder,
                'code': receipt_item.code,
                'name': receipt_item.name,
                'quantity': receipt_item.quantity,
                'price': receipt_item.price,
                'priceTotal': receipt_item.priceTotal,
                'orderlineNo': receipt_item.orderlineNo,   
                'size': receipt_item.size,   
                'color': receipt_item.color,              
                # Include other fields you want to retrieve
            }
            return JsonResponse(response_data)
        except ProductionReceiptItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})


from .models import SalesOrderItem,SalesOrderInfo
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
                    'lineNo': [item.lineNo for item in order_items],
                    'code': [item.code for item in order_items],
                    'name': [item.name for item in order_items],
                    'size': [item.size for item in order_items],
                    'color': [item.color for item in order_items],
                    'style': [item.style for item in order_items]
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




@csrf_exempt
def orderline_by_data(request):
    if request.method == 'POST':
        orderno = request.POST.get('orderno')
        orderlineNo = request.POST.get('orderlineNo')

        # Replace the filter conditions with the ones you need
        try:
            order_item = SalesOrderItem.objects.get(docNo=orderno, lineNo=orderlineNo)
            response_data = {
                
                'size': order_item.size,
                'color': order_item.color
            }
            return JsonResponse(response_data)
        except SalesOrderItem.DoesNotExist:
            return JsonResponse({'error': 'No data found for the given orderno and orderlineNo'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def deliveryinfo(request):
    if request.method == 'POST':
        orderno = int(request.POST.get('orderNo')) 
        

        # Replace the filter conditions with the ones you need
        try:
            orderinfo = SalesOrderInfo.objects.get(docNo=orderno)
            response_data = {
                
                'customerName': orderinfo.customerName.name,
                'address':orderinfo.address,
                'sales_employee':orderinfo.sales_employee.id,
                'remarks':orderinfo.remarks
                
            }
            return JsonResponse(response_data)
        except SalesOrderInfo.DoesNotExist:
            return JsonResponse({'error': 'No data found for the given orderno and orderlineNo'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

