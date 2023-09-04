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
                'name': item.name
                
                
                


            }
            return JsonResponse(response_data)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})

    return JsonResponse({'error': 'Invalid request method'})        