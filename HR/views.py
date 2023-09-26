from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse,HttpRequest,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance,Employee,OvertimeRecord,LeaveRequest,Payroll,Holiday,Resignation,Lefty
from django.db.models import Count, Sum,F,Q,Case, When, IntegerField
from datetime import date,timedelta,datetime
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm,DateFilterForm,YearFilterForm,EmployeeIDDateFilterForm,AttendanceUploadForm
import csv
import pandas as pd
from django.db import models

from collections import defaultdict


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




def upload_overtime_record(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Read the uploaded Excel file
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Loop through the data and create overtime_record_log objects
            for index, row in df.iterrows():
                id_no = row['employee_id']
                date_with_time = row['date'].strftime('%Y-%m-%d')
                othour = row['ot_hour']
                # Convert the 'date_with_time' string to a datetime object
                date = datetime.strptime(date_with_time, '%Y-%m-%d')
               
                # Assuming employee_id uniquely identifies an employee
                employee = Employee.objects.get(id_no=id_no)
                # Check if an Attendance record with the same date and employee already exists
                existing_record = OvertimeRecord.objects.filter(date=date, employee=employee).first()
                if not existing_record:            
                # Create an Attendance record with intime and outtime
                # Create an overtime_record_log object
                    overtime_record_log = OvertimeRecord.objects.create(
                        employee=employee,
                        date=date,
                        othour=othour,
                        id_no=id_no,
                        # Add more fields as needed
                    )

            return render(request, 'success_page.html')  # Redirect to a success page
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_overtime_record.html', {'form': form})

def attendance_report(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filter active employees
            active_employees = Employee.objects.filter(active=True)

            # Calculate absenteeism for each active employee
            attendance_report_data = []
            for employee in active_employees:
                absences = Attendance.objects.filter(
                    employee=employee,
                    date__range=(start_date, end_date),
                    status='Absent'
                ).count()
                
                present = Attendance.objects.filter(
                    employee=employee,
                    date__range=(start_date, end_date),
                    status='Present'
                ).count()       
                
                leave = Attendance.objects.filter(
                    employee=employee,
                    date__range=(start_date, end_date),
                    status='Leave'
                ).count() 
                                         
                attendance_report_data.append({
                    'employee_name': f"{employee.first_name} {employee.last_name}",
                    'absent_count': absences,
                    'present_count':present,
                    'leave_count':leave,                    
                })

            return render(request, 'attendance_report.html', {
                'attendance_report_data': attendance_report_data
            })
    else:
        form = DateFilterForm()

    return render(request, 'attendance_report.html', {'form': form})












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

def employee_leave_records_report(request):
    form = EmployeeIDDateFilterForm(request.POST or None)
    leave_records = None
    total_casual_leave = 0
    total_medical_leave = 0

    if request.method == 'POST' and form.is_valid():
        id_no = form.cleaned_data['id_no']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Filter LeaveRequest records by id_no and date range
        leave_records = LeaveRequest.objects.filter(
            employee__id_no=id_no,
            start_date__gte=start_date,
            end_date__lte=end_date
        )

        # Calculate the total sum of casual_leave and medical_leave
        total_casual_leave = leave_records.filter(leave_type='casual_leave').aggregate(Sum('leave_duration'))['leave_duration__sum'] or timedelta(0)
        total_medical_leave = leave_records.filter(leave_type='medical_leave').aggregate(Sum('leave_duration'))['leave_duration__sum'] or timedelta(0)

    return render(request, 'employee_leave_records_report.html', {
        'form': form,
        'leave_records': leave_records,
        'total_casual_leave': total_casual_leave,
        'total_medical_leave': total_medical_leave,
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
                ).aggregate(Sum('othour'))['othour__sum'] or 0

                summary_data.append({
                    'employee': employee,
                    'total_ot_hour': total_ot_hour,
                })
    return render(request, 'overtime_summary_report.html', {
        'form': form,
        'summary_data': summary_data,
    })

def overtime_summary_report_machine(request):
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
                total_ot_hour = Attendance.objects.filter(
                    employee=employee, date__gte=start_date, date__lte=end_date
                ).aggregate(Sum('othour'))['othour__sum'] or 0

                summary_data.append({
                    'employee': employee,
                    'total_ot_hour': total_ot_hour,
                })
    return render(request, 'overtime_summary_report_machine.html', {
        'form': form,
        'summary_data': summary_data,
    })
    
def employee_ot_hour_records_report(request):
    form = EmployeeIDDateFilterForm(request.POST or None)
    ot_hour_records = None
    employee_info = None
    total_ot_hours = 0

    if request.method == 'POST' and form.is_valid():
        id_no = form.cleaned_data['id_no']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        # Filter OvertimeRecord records by id_no and date range
        ot_hour_records = OvertimeRecord.objects.filter(
            employee__id_no=id_no,
            date__gte=start_date,
            date__lte=end_date
        )

        # Get employee information
        try:
            employee_info = Employee.objects.get(id_no=id_no)
        except Employee.DoesNotExist:
            employee_info = None
            
            
        # Calculate the total sum of ot_hour
        total_ot_hours = ot_hour_records.aggregate(Sum('othour'))['othour__sum'] or 0
        
    return render(request, 'employee_ot_hour_records_report.html', {
        'form': form,
        'ot_hour_records': ot_hour_records,
        'employee_info': employee_info,
        'total_ot_hours': total_ot_hours,
        
    })    
def upload_attendance(request):
    if request.method == 'POST':
        form = AttendanceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = form.cleaned_data['text_file']

            # Process the uploaded text file
            process_uploaded_file(text_file)

            return render(request, 'success_page.html')  # Redirect to a success page
    else:
        form = AttendanceUploadForm()
    return render(request, 'upload_attendance.html', {'form': form})

def process_uploaded_file(text_file):
    attendance_data = defaultdict(list)  # Use a defaultdict to group data by 'id_no' and 'date'

    # Read the uploaded data and process it
    lines = text_file.read().decode().splitlines()
    lines = lines[1:]  # Remove the header line

    for line in lines:
        parts = line.strip().split()
        id_number, date_str, time_str = parts[0], parts[1], parts[2] + ' ' + parts[3]  # Extract date and time parts

        # Combine date and time as a single string
        date_time_str = f"{date_str} {time_str}"

        # Parse date and time, considering AM/PM format
        date_time = datetime.strptime(date_time_str, '%m/%d/%Y %I:%M %p')

        # Convert to 24-hour format and extract time as a string
        date_time_24hr = date_time.strftime('%m/%d/%Y %H:%M')
        time_str_24hr = date_time.strftime('%H:%M')

        # Group data by 'id_no' and 'date'
        key = (id_number, date_time.date())
        attendance_data[key].append(date_time_24hr)

    # Insert data into the Django Attendance model
    for key, time_list in attendance_data.items():
        id_number, date = key
        if len(time_list) >= 1:
            intime = min(time_list)  # Get the earliest time as 'intime'
            outtime = max(time_list)  # Get the latest time as 'outtime'
            
            # Replace with code to fetch or create an Employee object based on id_number
            try:
                default_employee = Employee.objects.get(id_no=id_number)
            except Employee.DoesNotExist:
                # Handle the case where the Employee does not exist or create one
                default_employee = Employee.objects.create(id_no=id_number)
            # Check if an Attendance record with the same date and employee already exists
            existing_attendance = Attendance.objects.filter(date=date, employee=default_employee).first()
            if not existing_attendance:            
            # Create an Attendance record with intime and outtime
                Attendance.objects.create(
                    id_no=id_number,
                    date=date,
                    intime=datetime.strptime(intime, '%m/%d/%Y %H:%M').time(),
                    outtime=datetime.strptime(outtime, '%m/%d/%Y %H:%M').time(),
                    employee=default_employee,
                )
def update_holidays_status_view(request):
    if request.method == 'POST' and 'update_holidays_status_button' in request.POST:
        # Get all Attendance records with status 'Holiday'
        holiday_attendances = Attendance.objects.filter(status='Holiday')

        for attendance in holiday_attendances:
            date = attendance.date
            previous_day = date - timedelta(days=1)
            next_day = date + timedelta(days=1)

            is_previous_day_absent = Attendance.objects.filter(
                date=previous_day, status__in=['Present', 'Leave']
            ).exists()

            is_next_day_absent = Attendance.objects.filter(
                date=next_day, status__in=['Present', 'Leave']
            ).exists()

            if is_previous_day_absent and is_next_day_absent:
                # Update the status of the Attendance record to 'Absent'
                attendance.status = 'Holiday'
                attendance.save()
                
            else :    
                attendance.status = 'Absent'
                attendance.save()
        # Redirect to a success page or back to the same page
        return render(request, 'success_page.html')  # Redirect to a success page

    return render(request, 'update_holidays_status.html')     





def present_records_between_date(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            present_records = Attendance.objects.filter(
                date__range=[start_date, end_date],
                status='Present'
            )
            # Calculate the total sum of 'Present' records
            total_present = present_records.aggregate(total_present=Sum('id_no'))['total_present']
                        
            return render(request, 'present_records_between_date.html', {'present_records': present_records, 'total_present': total_present})
    else:
        form = DateFilterForm()
    return render(request, 'present_records_between_date.html', {'form': form})


def employees_without_present_records(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Retrieve employees who do not have 'Present' records within the date range
            employees_without_present_records = Employee.objects.exclude(
                attendance__date__range=[start_date, end_date],
                attendance__status='Present'
            )
            # Calculate the total count of 'id_no' for 'Absent' records
            total_absent_id_no = employees_without_present_records.aggregate(total_absent_id_no=Count('id_no'))['total_absent_id_no']        
            return render(request, 'employees_without_present_records.html', {'employees_without_present_records': employees_without_present_records, 'total_absent_id_no': total_absent_id_no})
    else:
        form = DateFilterForm()
    return render(request, 'employees_without_present_records.html', {'form': form})

def resignation_records_between_dates(request):
    resignations = []
    total_resignations = 0

    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filter Resignation records between the specified dates
            resignations = Resignation.objects.filter(
                resignation_date__range=[start_date, end_date]
            )
            total_resignations = resignations.count()

    else:
        form = DateFilterForm()

    context = {
        'form': form,
        'resignations': resignations,
        'total_resignations': total_resignations,
    }

    return render(request, 'resignation_records_between_dates.html', context)


def lefty_records_between_dates(request):
    lefties = []
    total_lefties = 0

    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filter Lefty records between the specified dates
            lefties = Lefty.objects.filter(
                left_date__range=[start_date, end_date]
            )
            total_lefties = lefties.count()

    else:
        form = DateFilterForm()

    context = {
        'form': form,
        'lefties': lefties,
        'total_lefties': total_lefties,
    }

    return render(request, 'lefty_records_between_dates.html', context)


def leave_request_records_between_dates(request):
    leave_requests = []
    total_leave_requests = 0

    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filter LeaveRequest records between the specified dates
            leave_requests = LeaveRequest.objects.filter(
                start_date__range=[start_date, end_date]
            )
            total_leave_requests = leave_requests.count()

    else:
        form = DateFilterForm()

    context = {
        'form': form,
        'leave_requests': leave_requests,
        'total_leave_requests': total_leave_requests,
    }

    return render(request, 'leave_request_records_between_dates.html', context)
from operator import itemgetter

def job_card(request):
    if request.method == 'POST':
        form = EmployeeIDDateFilterForm(request.POST)
        if form.is_valid():
            id_no = form.cleaned_data['id_no']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Initialize counters for 'P', 'A', and 'H'
            present_count = 0
            absent_count = 0
            holiday_count = 0
            leave_count = 0
            weekend_count = 0            
            # Create a list to store the results
            results = []

            # Loop through the dates in the specified range
            current_date = start_date
            while current_date <= end_date:
                try:
                    # Query the Attendance model to get the corresponding attendance record
                    attendance = Attendance.objects.get(employee__id_no=id_no, date=current_date)

                    # attendance.status
                    if attendance.status == 'Present':
                        status = 'P'  # Present
                        present_count += 1
                    elif attendance.status == 'Leave':
                        status = 'L'  # Leave
                        leave_count += 1
                    else:
                        # Check if the date is a holiday
                        is_holiday = Holiday.objects.filter(date=current_date).exists()
                        if is_holiday:
                            # Check if the previous day is a holiday
                            previous_day = current_date - timedelta(days=1)
                            is_previous_day_intime = Attendance.objects.get(employee__id_no=id_no, date=previous_day)                         
                            status = 'H'  # Holiday
                            holiday_count += 1
                        elif current_date.weekday() == 4:
                            status = 'W'  # Weekend
                            weekend_count += 1                                  
                        else:
                            status = 'A'  # Absent
                            absent_count += 1

                    # Append the result to the list
                    results.append({
                        'id_no': id_no,
                        'date': current_date,
                        'intime': attendance.intime,
                        'outtime': attendance.outtime,
                        'status': status,
                    })

                except Attendance.DoesNotExist:
                    # Check if the date is a holiday
                    is_holiday = Holiday.objects.filter(date=current_date).exists()
                    if is_holiday:
               
                            status = 'H'  # Holiday
                            holiday_count += 1
                    elif current_date.weekday() == 4:
                        status = 'W'  # Holiday   
                        weekend_count += 1                                                     
                    else:
                        status = 'A'  # Absent
                        absent_count += 1

                    # Append the result to the list
                    results.append({
                        'id_no': id_no,
                        'date': current_date,
                        'intime': None,
                        'outtime': None,
                        'status': status,
                    })

                # Move to the next date
                current_date += timedelta(days=1)

            # Calculate the total counts
            total_counts = {
                'Present': present_count,
                'Absent': absent_count,
                'Holiday': holiday_count,
                'Leave':leave_count,
                'Weeked': weekend_count 
            }

            return render(request, 'job_card.html', {'results': results, 'total_counts': total_counts})
    else:
        form = EmployeeIDDateFilterForm()

    return render(request, 'job_card.html', {'form': form})


from django.db.models import Count

def job_card_summary(request):
    if request.method == 'POST':
        form = DateFilterForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Step 1: Get the IDs of active employees
            active_employee_ids = Employee.objects.filter(active=True).values_list('id_no', flat=True)

            # Step 2: Filter the Attendance queryset for active employees and the date range
            attendance_queryset = Attendance.objects.filter(
                employee__id_no__in=active_employee_ids, date__range=(start_date, end_date)
            )

            # Create a dictionary to store the summary for each active employee
            employee_summary = {}

            # Step 3: Calculate the summary for each active employee
            for id_no in active_employee_ids:
                # Initialize counters for 'Present', 'Absent', 'Weekend', and 'Leave' for each employee
                present_count = 0
                absent_count = 0
                weekend_count = 0
                leave_count = 0

                # Loop through the dates in the specified range
                current_date = start_date
                while current_date <= end_date:
                    try:
                        # Query the Attendance queryset to get the corresponding attendance record
                        attendance = attendance_queryset.get(employee__id_no=id_no, date=current_date)

                        # Check if intime exists or status is 'Leave'
                        if attendance.status == 'Present': 
                           present_count += 1                            
                        elif  attendance.status == 'Leave':
                            leave_count += 1
                        else:
                            # Check if the date is a weekend
                            if current_date.weekday() == 4: # 
                                weekend_count += 1
                            else:
                                absent_count += 1

                    except Attendance.DoesNotExist:
                        # Check if the date is a weekend
                        if current_date.weekday() == 4:  # 5=Saturday, 6=Sunday
                            weekend_count += 1
                        else:
                            absent_count += 1

                    current_date += timedelta(days=1)

                # Calculate leave count by subtracting present count from the total days
                total_days = (end_date - start_date).days + 1
                leave_count = total_days - (present_count + weekend_count + absent_count)

                # Store the summary in the dictionary
                employee_summary[id_no] = {
                    'Present': present_count,
                    'Absent': absent_count,
                    'Weekend': weekend_count,
                    'Leave': leave_count,
                }

            return render(request, 'job_card_summary.html', {'employee_summary': employee_summary})
    else:
        form = DateFilterForm()

    return render(request, 'job_card_summary.html', {'form': form})
