from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta



class District(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class PoliceStation(models.Model):
    name = models.CharField(max_length=255)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    def __str__(self):
        return self.name    
     
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
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    hire_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    id_no = models.PositiveIntegerField(default=1, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)  # New field for active status
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    police_station = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, null=True, blank=True)
    
    address = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:

        verbose_name = 'Employee Master Data'
        verbose_name_plural = 'Employee Master Data'
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.skill.name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)    
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
    
class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50)
    document_file = models.FileField(upload_to='employee_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)    
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
        
        
        
        
class AttendanceLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    device_id = models.CharField(max_length=20)
    verification_type = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    work_code = models.CharField(max_length=20)
    department_id = models.CharField(max_length=20)
    shift_id = models.CharField(max_length=20)
    late_arrival = models.BooleanField(default=False)
    early_departure = models.BooleanField(default=False)
    overtime = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    holiday = models.BooleanField(default=False)
    leave_type = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(blank=True)
    sync_status = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.time_in} to {self.time_out}"        
    
    
class OvertimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_no = models.PositiveIntegerField(default=1, null=True, blank=True)
    date = models.DateField()
    ot_hour = models.DecimalField(max_digits=5, decimal_places=2)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)   
    def __str__(self):
        return f"Overtime Record for {self.employee.first_name} {self.employee.last_name} on {self.date}"    
    
    
    
    
    
    
    
    
    
    
    