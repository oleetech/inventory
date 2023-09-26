from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time
from django.utils import timezone




     
class Department(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )


    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    fatherName = models.CharField(max_length=100, blank=True, null=True)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    hire_date = models.DateField()
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    designation = models.CharField(max_length=100,blank=True, null=True)
    id_no = models.PositiveIntegerField(default=1, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    joiningSalary = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)  # New field for active status

    localAddress = models.CharField(max_length=200,blank=True, null=True)
    permanentAddress = models.CharField(max_length=200,blank=True, null=True)   
    photo = models.ImageField(upload_to='employee_photos/',null=True, blank=True)     
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:

        verbose_name = 'Employee Master Data'
        verbose_name_plural = 'Employee Master Data'
    def __str__(self):
        return f"{self.first_name} {self.last_name}"




    
    


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'),('Leave', 'Leave'),('Holiday', 'Holiday')],default='Present')
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    intime = models.TimeField(default=time(0, 0),blank=True)
    outtime = models.TimeField(default=time(0, 0),blank=True)  
    holiday_marked_as_holiday = models.BooleanField(default=False)
    othour = models.DurationField(default=timedelta(0))
    class Meta:
        unique_together = ('date', 'employee')        
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no


            
            
#OtHour
            
        # Convert intime and outtime to datetime objects with a fixed date (e.g., today's date)
        intime_datetime = datetime.combine(self.date, self.intime)
        outtime_datetime = datetime.combine(self.date, self.outtime)
        # Calculate the duration
        duration = outtime_datetime - intime_datetime
        
        # Calculate duty hours and OT hours based on conditions
        if intime_datetime.time() < time(9, 0):  # Before 9 am
            duty_hours = timedelta(hours=9)
        elif intime_datetime.time() >= time(13, 0):  # After 1 pm
            duty_hours = timedelta(hours=8)
        else:
            duty_hours = duration
            
        # Calculate overtime hours (othour)
        if duration > duty_hours:
            self.othour = duration - duty_hours
        else:
            self.othour = timedelta(0)
                        
                    

                                                    
        super().save(*args, **kwargs)    
 
        
            
class Holiday(models.Model):
    date = models.DateField()
    def __str__(self):
        return f"{self.id}"     
    

    
               
class LeaveRequest(models.Model):
    LEAVE_CHOICES = (
        ('casual_leave', 'Casual Leave'),
        ('medical_leave', 'Medical Leave'),
    )    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES, default='casual_leave')  # Set the default value
    leave_duration = models.DurationField(blank=True, null=True)
    
    reason = models.TextField()
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])  
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
            
        # Calculate the leave duration
        if self.start_date and self.end_date:
            self.leave_duration = self.end_date - self.start_date + timedelta(days=1)            
            
            
        super().save(*args, **kwargs)       
    class Meta:
        unique_together = ('start_date', 'end_date','employee')           
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    pay_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)    
    class Meta:
        unique_together = ('pay_date', 'employee')        
 
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    
    
class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    training_type = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.PositiveIntegerField()
    trainer = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    certificate = models.FileField(upload_to='employee_training_certificates/',null=True,blank=True)    
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)      
    class Meta:
        unique_together = ('date', 'employee')       
class EmployeePromotion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    promotion_date = models.DateField()
    previous_role = models.CharField(max_length=100)
    new_role = models.CharField(max_length=100)
    salary_change = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()    
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)        
  
class TaskAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])              
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)     
        
        
        
        

    
  
    
    
class OvertimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_no = models.PositiveIntegerField(default=1, null=True, blank=True)
    date = models.DateField()
    othour = models.DurationField(default=timedelta(0))
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)   
    def __str__(self):
        return f"Overtime Record for {self.employee.first_name} {self.employee.last_name} on {self.date}"    
    
    class Meta:
        unique_together = ('date', 'employee')     
    
    
class Award(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=100)
    giftItem = models.CharField(max_length=100)
    description = models.TextField()
    dateReceived = models.DateField()
    issuedBy = models.CharField(max_length=100)
    awardBy = models.CharField(max_length=100)

    def __str__(self):
        return self.title    
    
    
    
    
    
class Resignation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    resignation_date = models.DateField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)
    notice_period = models.PositiveIntegerField(default=30)  # You can change the default notice period as needed
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Resignation - {self.employee}"

    class Meta:
        verbose_name = 'Resignation'
        verbose_name_plural = 'Resignations'    
        
        
class Lefty(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    left_date = models.DateField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Approved')

    def __str__(self):
        return f"Lefty - {self.employee}"

    class Meta:
        verbose_name = 'Lefty'
        verbose_name_plural = 'Lefties'        