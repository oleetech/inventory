from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .models import BillOfMaterials,Production,ProductionComponent

def custom_print_view(request):
    model_name = request.GET.get('model_name')
    model_id = request.GET.get('model_id')

    # Fetch the object based on the model name and ID
    # Implement your printing logic here

    return HttpResponse(f'Printing {model_name} with ID {model_id}')

@csrf_exempt
def ajax_view(request):
    if request.method == 'POST':
        production_name  = request.POST.get('name')
        production_quantity  = request.POST.get('quantity')
        bill_of_materials = BillOfMaterials.objects.filter(name=production_name).first()
        if bill_of_materials:
            child_components = bill_of_materials.child_components.all()
            updated_components = []



            for component in child_components:
                if bill_of_materials.quantity == production_quantity:
                    updated_quantity = float(component.quantity)
                else:
                    updated_quantity = float(component.quantity) * (float(production_quantity) / float(bill_of_materials.quantity))
                updated_quantity = format(updated_quantity, '.4f')
                updated_components.append({
                    'id': component.id,
                    'code': component.code,
                    'name': component.name,
                    'uom': component.uom,
                    'quantity': updated_quantity
                })
                    

        return JsonResponse(updated_components, safe=False)

    return JsonResponse([], safe=False)


from .models import ProductionReceipt,ProductionReceiptItem

@csrf_exempt
def ajax_view_receipt(request):
    if request.method == 'POST':
        production = request.POST.get('productionNo')
      
        try:
            production_instance = Production.objects.get(docno=production)
            
            response_data = {
                'name': production_instance.name,
                'code': production_instance.code,
                'uom': production_instance.uom,
                
                'quantity':production_instance.quantity,
                'salesOrder': production_instance.salesOrder
            }
        except Production.DoesNotExist:
            response_data = {'error': 'Production not found'}
        
        return JsonResponse(response_data)

@csrf_exempt    
def get_production_order_info(request):
    if request.method == 'POST':
        docNo = request.POST.get('docNo')
        print("Received docNo:", docNo)  # Add this line for debugging
        try:
            order_items = ProductionComponent.objects.filter(docNo=docNo)

            if order_items.exists():  # Check if there are any results
                # Assuming you want to return a list of 'name' values for all matching rows
                response_data = {
                    'lineNo': [item.lineNo for item in order_items],
                    'code': [item.code for item in order_items],
                    'name': [item.name for item in order_items],

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