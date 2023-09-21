from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpRequest,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import PoliceStation,District,AttendanceLog,Attendance,Employee,OvertimeRecord

from django.shortcuts import render, redirect
from .forms import ExcelUploadForm,DateFilterForm
from .models import Payroll, Employee
import pandas as pd


# Create your views here.
def home(request):
    return render(request, 'hrindex.html')


    


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
                payroll = Payroll.objects.create(employee=employee, pay_date=date, amount=amount, id_no=id_no)

            return render(request,'success_page.html')  # Redirect to a success page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_payroll.html', {'form': form})


def upload_attendance(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Loop through the data and create AttendanceLog objects
            for index, row in df.iterrows():
                employee_id = row['employee_id']
                date = row['date']
                time_in = row['time_in']
                time_out = row['time_out']
                # Add more fields as needed

                # Assuming employee_id uniquely identifies an employee
                employee = Employee.objects.get(id_no=employee_id)

                # Create an AttendanceLog object
                attendance_log = AttendanceLog.objects.create(
                    employee=employee,
                    date=date,
                    time_in=time_in,
                    time_out=time_out,
                
                    # Add more fields as needed
                )

            return render(request, 'success_page.html')  # Redirect to a success page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_attendance.html', {'form': form})


def upload_overtime_record(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Loop through the data and create overtime_record_log objects
            for index, row in df.iterrows():
                employee_id = row['employee_id']
                date = row['date']
                ot_hour = row['ot_hour']

                # Add more fields as needed

                # Assuming employee_id uniquely identifies an employee
                employee = Employee.objects.get(id_no=employee_id)

                # Create an overtime_record_log object
                overtime_record_log = OvertimeRecord.objects.create(
                    employee=employee,
                    date=date,
                    ot_hour=ot_hour,
                    id_no=employee_id,
                    # Add more fields as needed
                )

            return render(request, 'success_page.html')  # Redirect to a success page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_overtime_record.html', {'form': form})

# def attendance_report(request):
#     if request.method == 'POST':
#         form = DateFilterForm(request.POST)
#         if form.is_valid():
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']

#             # Filter active employees
#             active_employees = Employee.objects.filter(active=True)

#             # Calculate absenteeism for each active employee
#             attendance_report_data = []
#             for employee in active_employees:
#                 absences = Attendance.objects.filter(
#                     employee=employee,
#                     date__range=(start_date, end_date),
#                     status='Absent'
#                 ).count()
#                 attendance_report_data.append({
#                     'employee_name': f"{employee.first_name} {employee.last_name}",
#                     'absent_count': absences
#                 })

#             return render(request, 'attendance_report.html', {
#                 'attendance_report_data': attendance_report_data
#             })
#     else:
#         form = DateFilterForm()

#     return render(request, 'attendance_report.html', {'form': form})