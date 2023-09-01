from django.shortcuts import render
from Production.models import Production,ProductionComponent  # Import your model

def send_data(request):
    # Simulate sending some data
    data = {'message': 'Hello, this is some data!'}
    
    # Render the HTML template and pass the data as context
    return render(request, 'print.html', {'data': data})
