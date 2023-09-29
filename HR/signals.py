from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .models import LeaveRequest,Attendance,Holiday,Employee,OvertimeRecord,Lefty
from datetime import datetime, timedelta, time
@receiver(post_save, sender=LeaveRequest)
def create_leave_attendance(sender, instance, created, **kwargs):
    if instance.status == 'Approved':
        # Create corresponding Attendance records for the date range of the LeaveRequest
        date_range = [instance.start_date, instance.end_date]
        for date in date_range:
            # Check if an Attendance record already exists for this date and employee
            existing_attendance = Attendance.objects.filter(
                date=date,
                employee=instance.employee,
            ).first()
            if not existing_attendance:
                # Create a new Attendance record with status "Leave"
                Attendance.objects.create(
                    employee=instance.employee,
                    date=date,
                    status="Leave",
                    id_no=instance.employee.id_no,
                    intime=time(0, 0),  # Set intime to midnight
                    outtime=time(0, 0),  # Set outtime to midnight     
                    department= instance.employee.department,              
                )
                
                

# Connect the signal handler function to the post_save signal for LeaveRequest
post_save.connect(create_leave_attendance, sender=LeaveRequest)

# @receiver(post_save, sender=Holiday)
# def create_holiday_attendance(sender, instance, created, **kwargs):
#     if created:
#         # Get all active employees
#         active_employees = Employee.objects.filter(active=True)

#         # Create corresponding Attendance records for each active employee on the holiday date
#         for employee in active_employees:
#             # Check if an Attendance record already exists for this date and employee
#             existing_attendance = Attendance.objects.filter(
#                 date=instance.date,
#                 employee=employee,
#             ).first()
#             if not existing_attendance:
#                 # Create a new Attendance record with status "Holiday"
#                 Attendance.objects.create(
#                     employee=employee,
#                     date=instance.date,
#                     status="Holiday",
#                     id_no=employee.id_no,
#                     intime=time(0, 0),  # Set intime to midnight
#                     outtime=time(0, 0),  # Set outtime to midnight                         
#                 )
                
                
@receiver(post_save, sender=Lefty)
def update_employee_active_status(sender, instance, **kwargs):
    if instance.status == 'Approved':
        instance.employee.active = False  # Set the employee's active status to False
        instance.employee.save()