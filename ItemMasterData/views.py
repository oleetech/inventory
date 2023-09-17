from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item

@csrf_exempt
def item(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            item = Item.objects.get(code=code)

            response_data = {
                'code': item.code,
                'name': item.name,
                'description': item.description,

                'unit_id': item.unit.id,
                'unit_name': item.unit.name,  # Assuming you want to include unit information
 
                'price': str(item.price),  # Convert DecimalField to a string for JSON serialization

            }
            return JsonResponse(response_data)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})        


@csrf_exempt
def item_name(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            item = Item.objects.get(name=name)

            response_data = {
                'code': item.code,
                'name': item.name,


            }
            return JsonResponse(response_data)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})    

  