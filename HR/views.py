from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpRequest,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import AttendanceLog,Attendance,Employee,OvertimeRecord,LeaveRequest
from django.db.models import Count, Sum
from datetime import date
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm,DateFilterForm,YearFilterForm
from .models import Payroll, Employee
import pandas as pd
from django.db import models


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




def attendance_summary_report(request):


    if request.method == 'POST':
        # If the form is submitted, validate the data.
        form = DateFilterForm(request.POST)
        if form.is_valid():
            # Get the start_date and end_date from the form.
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Query to calculate attendance statistics for each employee within the specified time period
            # and whose status is True.
            attendance_summary = Employee.objects.filter(active=True).annotate(
                total_days_present=Count('attendancelog', filter=models.Q(attendancelog__date__range=[start_date, end_date], attendancelog__status='Present')),
                total_days_absent=Count('attendancelog', filter=models.Q(attendancelog__date__range=[start_date, end_date], attendancelog__status='Absent')),
                total_days_late=Count('attendancelog', filter=models.Q(attendancelog__date__range=[start_date, end_date], attendancelog__late_arrival=True)),
                total_days_on_leave=Count('attendancelog', filter=models.Q(attendancelog__date__range=[start_date, end_date], attendancelog__leave_type__isnull=False))
            )

            return render(request, 'attendance_summary_report.html', {'attendance_summary': attendance_summary, 'form': form})
    # Initialize the form with default values.
    form = DateFilterForm()
    return render(request, 'attendance_summary_report.html', {'form': form})






# ...
from django.db.models import F

def leave_balance_report(request):
    # Initialize the form with default values.
    form = YearFilterForm(request.GET or None)

    # Initialize leave quantities and balance quantities for each type
    leave_data = []

    if request.method == 'POST':
        # If the form is submitted, validate the data.
        form = YearFilterForm(request.POST)
        if form.is_valid():
            selected_year = form.cleaned_data['year']
            start_date = date(selected_year, 1, 1)
            end_date = date(selected_year, 12, 31)

            # Get all employees
            employees = Employee.objects.filter(active=True)

            # Calculate leave quantities and balance quantities for each leave type
            for employee in employees:
                # Calculate accrued leave for casual_leave
                casual_leave_requests = LeaveRequest.objects.filter(
                    employee=employee, leave_type='casual_leave', status='Approved', start_date__year=selected_year
                ).aggregate(Sum('leave_duration'))
                casual_leave_quantity = casual_leave_requests['leave_duration__sum'].days if casual_leave_requests['leave_duration__sum'] else 0

                # Calculate accrued leave for medical_leave
                medical_leave_requests = LeaveRequest.objects.filter(
                    employee=employee, leave_type='medical_leave', status='Approved', start_date__year=selected_year
                ).aggregate(Sum('leave_duration'))
                medical_leave_quantity = medical_leave_requests['leave_duration__sum'].days if medical_leave_requests['leave_duration__sum'] else 0

                # Calculate balance quantities
                casual_leave_balance = 10 - casual_leave_quantity
                medical_leave_balance = 15 - medical_leave_quantity

                leave_data.append({
                    'employee': employee,
                    'casual_leave_quantity': casual_leave_quantity,
                    'medical_leave_quantity': medical_leave_quantity,
                    'casual_leave_balance': casual_leave_balance,
                    'medical_leave_balance': medical_leave_balance,
                })

    return render(request, 'leave_balance_report.html', {
        'form': form,
        'leave_data': leave_data,
    })





def overtime_summary_report(request):
    form = DateFilterForm(request.GET or None)

    summary_data = []

    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Get active employees
            employees = Employee.objects.filter(active=True)

            for employee in employees:
                # Calculate total ot_hour within the date range
                total_ot_hour = OvertimeRecord.objects.filter(
                    employee=employee, date__gte=start_date, date__lte=end_date
                ).aggregate(Sum('ot_hour'))['ot_hour__sum'] or 0

                summary_data.append({
                    'employee': employee,
                    'total_ot_hour': total_ot_hour,
                })
    return render(request, 'overtime_summary_report.html', {
        'form': form,
        'summary_data': summary_data,
    })