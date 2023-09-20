from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpRequest,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import PoliceStation,District
# Create your views here.
def home(request):
    return HttpResponse('Hr')
@csrf_exempt
def policestation(request):
    if request.method == 'POST':
        districtId = int(request.POST.get('district')) 
        

        # Replace the filter conditions with the ones you need
        try:
            # district = District.objects.get(id=districtId)
            
            police_stations = PoliceStation.objects.filter(district__id=districtId)
            police_station_names = [station.name for station in police_stations]
            response_data = {
                
                'police_stations': police_station_names,

                
            }
            return JsonResponse(response_data)
        except PoliceStation.DoesNotExist:
            return JsonResponse({'error': 'No data found for the given orderno and orderlineNo'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    

    
# employees/views.py

from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import Payroll, Employee
import pandas as pd

def upload_payroll(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Loop through the data and create Payroll objects
            for index, row in df.iterrows():
                id_no = row['id_no']
                date = row['date']
                amount = row['amount']

                # Assuming id_no uniquely identifies an employee
                employee = Employee.objects.get(id_no=id_no)

                # Create a Payroll object
                payroll = Payroll.objects.create(employee=employee, pay_date=date, amount=amount)

            return render(request,'success_page.html')  # Redirect to a success page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_payroll.html', {'form': form})
