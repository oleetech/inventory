from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time
from django.utils import timezone

'''
  ____                 _                           _     _                 
 |  _ \    ___   ___  (_)   __ _   _ __     __ _  | |_  (_)   ___    _ __  
 | | | |  / _ \ / __| | |  / _` | | '_ \   / _` | | __| | |  / _ \  | '_ \ 
 | |_| | |  __/ \__ \ | | | (_| | | | | | | (_| | | |_  | | | (_) | | | | |
 |____/   \___| |___/ |_|  \__, | |_| |_|  \__,_|  \__| |_|  \___/  |_| |_|
                           |___/                                           

'''

class Designation(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
'''
  ____                                  _                                _   
 |  _ \    ___   _ __     __ _   _ __  | |_   _ __ ___     ___   _ __   | |_ 
 | | | |  / _ \ | '_ \   / _` | | '__| | __| | '_ ` _ \   / _ \ | '_ \  | __|
 | |_| | |  __/ | |_) | | (_| | | |    | |_  | | | | | | |  __/ | | | | | |_ 
 |____/   \___| | .__/   \__,_| |_|     \__| |_| |_| |_|  \___| |_| |_|  \__|
                |_|                                                          
'''     
class Department(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

'''
  ____    _       _    __   _   
 / ___|  | |__   (_)  / _| | |_ 
 \___ \  | '_ \  | | | |_  | __|
  ___) | | | | | | | |  _| | |_ 
 |____/  |_| |_| |_| |_|    \__|
                                
'''    
class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name

'''
  _____                       _                               
 | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___ 
 |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \
 | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/
 |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___|
                     |_|                  |___/               

'''    
class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    RELIGION_CHOICES = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('Buddhism', 'Buddhism'),
        ('Sikhism', 'Sikhism'),
        ('Judaism', 'Judaism'),
        ('Other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]



    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    fatherName = models.CharField(max_length=100, blank=True, null=True)
    motherName = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    hire_date = models.DateField()
    designation = models.CharField(max_length=100,blank=True, null=True)
    id_no = models.PositiveIntegerField(default=1, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    joiningSalary = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    nid = models.CharField(max_length=30, blank=True, null=True)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=False)  # New field for active status
    bloodGroup = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES,blank=True, null=True)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES,blank=True, null=True)
    # Define the marital_status field with choices
    maritalStatus = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES,blank=True, null=True)
    localAddress = models.CharField(max_length=200,blank=True, null=True)
    permanentAddress = models.CharField(max_length=200,blank=True, null=True)   
    photo = models.ImageField(upload_to='employee_photos/',null=True, blank=True)     
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, default=None)    
    class Meta:
        verbose_name = 'Employee Master Data'
        verbose_name_plural = 'Employee Master Data'
            
    def __str__(self):
        return f"{self.id_no}"  
class NomineeInformation(models.Model):


    RELATIONSHIP_CHOICES = (
        ('Spouse', 'Spouse'),
        ('Child', 'Child'),
        ('Parent', 'Parent'),
        ('Sibling', 'Sibling'),
        ('Other', 'Other'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    nid = models.CharField(max_length=30, blank=True, null=True)
    relationship = models.CharField(max_length=10, choices=RELATIONSHIP_CHOICES)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.employee.id_no}"     
'''
  _____                       _                                 ____                                                      _   
 | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___  |  _ \    ___     ___   _   _   _ __ ___     ___   _ __   | |_ 
 |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \ | | | |  / _ \   / __| | | | | | '_ ` _ \   / _ \ | '_ \  | __|
 | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/ | |_| | | (_) | | (__  | |_| | | | | | | | |  __/ | | | | | |_ 
 |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___| |____/   \___/   \___|  \__,_| |_| |_| |_|  \___| |_| |_|  \__|
                     |_|                  |___/                                                                               

'''
class EmployeeDocument(models.Model):
    EMPLOYEE_DOCUMENT_TYPES = (
        ('Resume', 'Resume'),
        ('Contract', 'Contract'),
        ('ID Card', 'ID Card'),
        ('Other', 'Other'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Associate the document with an employee (User model in this case)
    document_name = models.CharField(max_length=100)
    document_type = models.CharField(max_length=20, choices=EMPLOYEE_DOCUMENT_TYPES)
    upload_date = models.DateTimeField(auto_now_add=True)
    document_file = models.FileField(upload_to='employee_documents/')

    def __str__(self):
        return self.document_name  

    
class EducationInformation(models.Model):
    # Existing fields
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)    
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    completion_year = models.PositiveIntegerField()  
    def __str__(self):
        return f'{self.employee.id_no}'      
class ExperienceInformation(models.Model):
    # Existing fields
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    education_info = models.ForeignKey(EducationInformation, on_delete=models.CASCADE, related_name='experiences')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)    
    def save(self, *args, **kwargs):
  
        if not self.employee :
            self.employee = self.education_info.employee  
            
        super().save(*args, **kwargs)  
        
class EmployeeBankInfo(models.Model):
    BANK_CHOICES = (
    ('Bank A', 'Bank A'),
    ('Bank B', 'Bank B'),
    ('Bank C', 'Bank C'),
    ('Bank D', 'Bank D'),
    # Add more banks as needed
)
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_info')
    account_number = models.CharField(max_length=20)
    bank_name = models.CharField(max_length=50, choices=BANK_CHOICES)     
    
    def __str__(self):
        return f" {self.employee.name}"       
class PersonalFileChecklist(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  
    photo = models.BooleanField(default=False)
    cv = models.BooleanField(default=False)
    bdc = models.BooleanField(default=False)
    eduCertificate = models.BooleanField(default=False)
    expCertificate = models.BooleanField(default=False)
    ageverification = models.BooleanField(default=False)
    testreport = models.BooleanField(default=False)
    jobdetails = models.BooleanField(default=False)
    referenceConfermation = models.BooleanField(default=False)
    nominidoc = models.BooleanField(default=False)
    chairmancertificate = models.BooleanField(default=False)
    backgroundchecklist = models.BooleanField(default=False)
    appoinmentletter = models.BooleanField(default=False)
    confirmationletter = models.BooleanField(default=False)
    officeidcardcopy = models.BooleanField(default=False)
    incrementlettercopy = models.BooleanField(default=False)
    leaverecord = models.BooleanField(default=False)
    signaturecopy = models.BooleanField(default=False)

    def __str__(self):
        return f"Checklist for {self.employee}"

    class Meta:
        verbose_name_plural = "Personal File Checklists"                              
'''
     _      _     _                        _                               
    / \    | |_  | |_    ___   _ __     __| |   __ _   _ __     ___    ___ 
   / _ \   | __| | __|  / _ \ | '_ \   / _` |  / _` | | '_ \   / __|  / _ \
  / ___ \  | |_  | |_  |  __/ | | | | | (_| | | (_| | | | | | | (__  |  __/
 /_/   \_\  \__|  \__|  \___| |_| |_|  \__,_|  \__,_| |_| |_|  \___|  \___|
                                                                           
'''

class Attendanceinfo(models.Model):
    date = models.DateField(default=timezone.now)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    
    def __str__(self):
        return f'{self.date}'    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance=models.ForeignKey(Attendanceinfo, on_delete=models.CASCADE, null=True, default=None)  
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'),('Leave', 'Leave'),('Holiday', 'Holiday')],default='Present')
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    intime = models.TimeField(default=time(8, 0),blank=True)
    outtime = models.TimeField(default=time(17, 0),blank=True)  
    holiday_marked_as_holiday = models.BooleanField(default=False)
    othour = models.DurationField(default=timedelta(0))
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    

     
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        # If the shift is not set explicitly, set it based on the employee's shift
        if not self.shift and self.employee:
            self.shift = self.employee.shift    
        if not self.department and    not self.department:
            self.department = self.employee.department                      

  
            
            
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
 
        
    def __str__(self):
        return f'{self.id_no}' 
    
    
'''
   ___                          _     _                      ____                                     _ 
  / _ \  __   __   ___   _ __  | |_  (_)  _ __ ___     ___  |  _ \    ___    ___    ___    _ __    __| |
 | | | | \ \ / /  / _ \ | '__| | __| | | | '_ ` _ \   / _ \ | |_) |  / _ \  / __|  / _ \  | '__|  / _` |
 | |_| |  \ V /  |  __/ | |    | |_  | | | | | | | | |  __/ |  _ <  |  __/ | (__  | (_) | | |    | (_| |
  \___/    \_/    \___| |_|     \__| |_| |_| |_| |_|  \___| |_| \_\  \___|  \___|  \___/  |_|     \__,_|
                                                                                                        

'''    
    
class OvertimeRecordinfo(models.Model):
    date = models.DateField(default=timezone.now)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    
    def __str__(self):
        return f'{self.date}'    
    
class OvertimeRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    overtimeinfo=models.ForeignKey(OvertimeRecordinfo, on_delete=models.CASCADE, null=True, default=None,blank=True)  
    
    id_no = models.PositiveIntegerField(default=1, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    othour = models.PositiveIntegerField(default=0, null=True, blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        if not self.date:
            self.date = self.employee.date   
        if not self.department :
            self.department = self.overtimeinfo.department       
                           
        super().save(*args, **kwargs)   
    def __str__(self):
        return f"Overtime Record for {self.employee.first_name} {self.employee.last_name} on {self.date}"    
    
    class Meta:
        unique_together = ('date', 'employee')     

'''
  _   _           _   _       _                 
 | | | |   ___   | | (_)   __| |   __ _   _   _ 
 | |_| |  / _ \  | | | |  / _` |  / _` | | | | |
 |  _  | | (_) | | | | | | (_| | | (_| | | |_| |
 |_| |_|  \___/  |_| |_|  \__,_|  \__,_|  \__, |
                                          |___/ 

'''                    
class Holiday(models.Model):
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.id}"     
    

    
'''
  _                                     ____                                        _   
 | |       ___    __ _  __   __   ___  |  _ \    ___    __ _   _   _    ___   ___  | |_ 
 | |      / _ \  / _` | \ \ / /  / _ \ | |_) |  / _ \  / _` | | | | |  / _ \ / __| | __|
 | |___  |  __/ | (_| |  \ V /  |  __/ |  _ <  |  __/ | (_| | | |_| | |  __/ \__ \ | |_ 
 |_____|  \___|  \__,_|   \_/    \___| |_| \_\  \___|  \__, |  \__,_|  \___| |___/  \__|
                                                          |_|                           

'''               
class LeaveRequest(models.Model):
    LEAVE_CHOICES = (
        ('casual_leave', 'Casual Leave'),
        ('medical_leave', 'Medical Leave'),
    )    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
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
        
'''
  ____                                   _   _ 
 |  _ \    __ _   _   _   _ __    ___   | | | |
 | |_) |  / _` | | | | | | '__|  / _ \  | | | |
 |  __/  | (_| | | |_| | | |    | (_) | | | | |
 |_|      \__,_|  \__, | |_|     \___/  |_| |_|
                  |___/                        

'''                 
class Payroll(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True) 
    created = models.DateField(default=timezone.now)
    docNo = models.PositiveIntegerField(default=1, unique=True)
    totalAmount = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True,default=0)
    
    def __str__(self):
        return f" {self.docNo}"    
    
class PayrollItem(models.Model):    
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, null=True, default=None)             
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)      
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True) 
    created = models.DateField(default=timezone.now)    
    docNo = models.PositiveIntegerField(default=1, unique=False)
    def __str__(self):
        return f" {self.docNo}"    
     
'''
     _                                                                                       ____  
    / \     _ __    _ __     ___    _   _   _ __     ___    ___   _ __ ___     ___   _ __   | ___| 
   / _ \   | '_ \  | '_ \   / _ \  | | | | | '_ \   / __|  / _ \ | '_ ` _ \   / _ \ | '_ \  |___ \ 
  / ___ \  | | | | | | | | | (_) | | |_| | | | | | | (__  |  __/ | | | | | | |  __/ | | | |  ___) |
 /_/   \_\ |_| |_| |_| |_|  \___/   \__,_| |_| |_|  \___|  \___| |_| |_| |_|  \___| |_| |_| |____/ 
                                                                                                   

''' 
class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    
'''
  _____                       _                                 _____                  _           _                 
 | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___  |_   _|  _ __    __ _  (_)  _ __   (_)  _ __     __ _ 
 |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \   | |   | '__|  / _` | | | | '_ \  | | | '_ \   / _` |
 | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/   | |   | |    | (_| | | | | | | | | | | | | | | (_| |
 |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___|   |_|   |_|     \__,_| |_| |_| |_| |_| |_| |_|  \__, |
                     |_|                  |___/                                                                |___/ 
'''    
class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    training_type = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
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
        
'''
  _____                       _                                 ____                                       _     _                 
 | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___  |  _ \   _ __    ___    _ __ ___     ___   | |_  (_)   ___    _ __  
 |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \ | |_) | | '__|  / _ \  | '_ ` _ \   / _ \  | __| | |  / _ \  | '_ \ 
 | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/ |  __/  | |    | (_) | | | | | | | | (_) | | |_  | | | (_) | | | | |
 |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___| |_|     |_|     \___/  |_| |_| |_|  \___/   \__| |_|  \___/  |_| |_|
                     |_|                  |___/                                                                                    

'''         
class EmployeePromotion(models.Model):
    docNo = models.PositiveIntegerField(default=1, unique=True)
    created = models.DateField(default=timezone.now)    
             
class EmployeePromotionItem(models.Model):  
    promotion = models.ForeignKey(EmployeePromotion, on_delete=models.CASCADE, null=True, default=None)             
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE,blank=True, null=True)  
    promotion_date = models.DateField(default=timezone.now) 
    previous_role = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, default=Designation.objects.first(), related_name='previous_promotions')
    new_role = models.ForeignKey(Designation, on_delete=models.CASCADE, null=True, default=Designation.objects.first(), related_name='new_promotions')
    salary_change = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()    
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)        

    created = models.DateField(default=timezone.now)    
    docNo = models.PositiveIntegerField(default=1, unique=False)
    
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
            
            
        if not self.created:
            self.created = self.promotion.created    
        if not self.docNo:
            self.docNo = self.promotion.docNo   
            
        super().save(*args, **kwargs)      
    def __str__(self):
        return f" {self.docNo}"  
'''
  _____                 _         _                  _                                              _   
 |_   _|   __ _   ___  | | __    / \     ___   ___  (_)   __ _   _ __    _ __ ___     ___   _ __   | |_ 
   | |    / _` | / __| | |/ /   / _ \   / __| / __| | |  / _` | | '_ \  | '_ ` _ \   / _ \ | '_ \  | __|
   | |   | (_| | \__ \ |   <   / ___ \  \__ \ \__ \ | | | (_| | | | | | | | | | | | |  __/ | | | | | |_ 
   |_|    \__,_| |___/ |_|\_\ /_/   \_\ |___/ |___/ |_|  \__, | |_| |_| |_| |_| |_|  \___| |_| |_|  \__|
                                                         |___/                                          

'''       
class TaskAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField(default=timezone.now)
    status = models.CharField(max_length=15, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])              
    id_no = models.PositiveIntegerField(default=1, null=True,blank=True)
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
        super().save(*args, **kwargs)     
        
        
        
        

    
  
'''
     _                                    _ 
    / \    __      __   __ _   _ __    __| |
   / _ \   \ \ /\ / /  / _` | | '__|  / _` |
  / ___ \   \ V  V /  | (_| | | |    | (_| |
 /_/   \_\   \_/\_/    \__,_| |_|     \__,_|
                                            

'''
    
class Award(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=100)
    giftItem = models.CharField(max_length=100)
    description = models.TextField()
    dateReceived = models.DateField(default=timezone.now)
    issuedBy = models.CharField(max_length=100)
    awardBy = models.CharField(max_length=100)

    def __str__(self):
        return self.title    
    
    
    
    
'''
  ____                 _                           _     _                 
 |  _ \    ___   ___  (_)   __ _   _ __     __ _  | |_  (_)   ___    _ __  
 | |_) |  / _ \ / __| | |  / _` | | '_ \   / _` | | __| | |  / _ \  | '_ \ 
 |  _ <  |  __/ \__ \ | | | (_| | | | | | | (_| | | |_  | | | (_) | | | | |
 |_| \_\  \___| |___/ |_|  \__, | |_| |_|  \__,_|  \__| |_|  \___/  |_| |_|
                           |___/                                           

'''    
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
        
'''
  _               __   _           
 | |       ___   / _| | |_   _   _ 
 | |      / _ \ | |_  | __| | | | |
 | |___  |  __/ |  _| | |_  | |_| |
 |_____|  \___| |_|    \__|  \__, |
                             |___/ 

'''        
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
        
        

'''
  _____                       _                                 _                             
 | ____|  _ __ ___    _ __   | |   ___    _   _    ___    ___  | |       ___     __ _   _ __  
 |  _|   | '_ ` _ \  | '_ \  | |  / _ \  | | | |  / _ \  / _ \ | |      / _ \   / _` | | '_ \ 
 | |___  | | | | | | | |_) | | | | (_) | | |_| | |  __/ |  __/ | |___  | (_) | | (_| | | | | |
 |_____| |_| |_| |_| | .__/  |_|  \___/   \__, |  \___|  \___| |_____|  \___/   \__,_| |_| |_|
                     |_|                  |___/                                               

'''    
    
class EmployeeLoan(models.Model):
    EMPLOYEE_LOAN_TYPES = (
        ('Personal', 'Personal Loan'),
        ('Home', 'Home Loan'),
        ('Car', 'Car Loan'),
        ('Education', 'Education Loan'),
        ('Other', 'Other Loan'),
    )
    APPROVAL_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=EMPLOYEE_LOAN_TYPES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='Pending')
    repayment_terms = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_complete = models.BooleanField(default=False)

    def update_loan_status(self):
        total_repayment_amount = sum(repayment.repayment_amount for repayment in self.loanrepayment_set.all())
        if total_repayment_amount >= self.loan_amount:
            self.is_complete = True
        else:
            self.is_complete = False
        self.save()
            
    def get_due_amount(self):
        repayments = LoanRepayment.objects.filter(loan=self)
        total_repayments = sum(repayment.repayment_amount for repayment in repayments)
        return self.loan_amount - total_repayments
    def __str__(self):
        return f"{self.employee} - {self.loan_type} Loan"
    class Meta:

        verbose_name = 'Employee Loan Pay'
        verbose_name_plural = 'Employee Loan Pay'       
'''
  _                               ____                                                              _   
 | |       ___     __ _   _ __   |  _ \    ___   _ __     __ _   _   _   _ __ ___     ___   _ __   | |_ 
 | |      / _ \   / _` | | '_ \  | |_) |  / _ \ | '_ \   / _` | | | | | | '_ ` _ \   / _ \ | '_ \  | __|
 | |___  | (_) | | (_| | | | | | |  _ <  |  __/ | |_) | | (_| | | |_| | | | | | | | |  __/ | | | | | |_ 
 |_____|  \___/   \__,_| |_| |_| |_| \_\  \___| | .__/   \__,_|  \__, | |_| |_| |_|  \___| |_| |_|  \__|
                                                |_|              |___/                                  

'''
class LoanRepayment(models.Model):
    loan = models.ForeignKey(EmployeeLoan, on_delete=models.CASCADE)
    repayment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    repayment_date = models.DateField()
    
    def save(self, *args, **kwargs):
        super(LoanRepayment, self).save(*args, **kwargs)
        self.loan.update_loan_status()
            
    def __str__(self):
        return f"Repayment for {self.loan} on {self.repayment_date}"           
    
    class Meta:

        verbose_name = 'Employee Loan Received'
        verbose_name_plural = 'Employee Loan Received'    