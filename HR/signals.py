from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .models import LeaveRequest,Attendance,Holiday,Employee,OvertimeRecord
from datetime import datetime, timedelta, time
@receiver(post_save, sender=LeaveRequest)
def create_leave_attendance(sender, instance, created, **kwargs):
    if created:
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
                )

# Connect the signal handler function to the post_save signal for LeaveRequest
post_save.connect(create_leave_attendance, sender=LeaveRequest)

@receiver(post_save, sender=Holiday)
def create_holiday_attendance(sender, instance, created, **kwargs):
    if created:
        # Get all active employees
        active_employees = Employee.objects.filter(active=True)

        # Create corresponding Attendance records for each active employee on the holiday date
        for employee in active_employees:
            # Check if an Attendance record already exists for this date and employee
            existing_attendance = Attendance.objects.filter(
                date=instance.date,
                employee=employee,
            ).first()
            if not existing_attendance:
                # Create a new Attendance record with status "Holiday"
                Attendance.objects.create(
                    employee=employee,
                    date=instance.date,
                    status="Holiday",
                    id_no=employee.id_no,
                    intime=time(0, 0),  # Set intime to midnight
                    outtime=time(0, 0),  # Set outtime to midnight                         
                )
                
                
@receiver(post_save, sender=OvertimeRecord)
def update_attendance_othour(sender, instance, **kwargs):
    try:
        # Try to get an Attendance record with matching id_no and date
        attendance_record = Attendance.objects.get( id_no=instance.id_no, date=instance.date)
        
        # Update the othour field in Attendance with the value from OvertimeRecord
        attendance_record.othour = instance.othour
        attendance_record.save()
    except Attendance.DoesNotExist:
        pass  # No matching Attendance record found, do nothing     
    
# Connect the signal handler function to the post_save signal for LeaveRequest
post_save.connect(update_attendance_othour, sender=OvertimeRecord)            