from django.contrib import admin
from .models import Employee,Department,Attendance, LeaveRequest, Payroll,  Announcement,EmployeeTraining, EmployeePromotion, TaskAssignment,OvertimeRecord,Holiday,Resignation,Lefty
from django import forms
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Register your models here.
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['owner',]  # You can exclude fields if needed

        widgets = {
            # 'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
        }  
@admin.register(Employee)                             
class EmployeeAdmin(admin.ModelAdmin):
  
    form = EmployeeForm  
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'     
    class Media: 
        js = ('js/employee.js','bootstrap.bundle.min.js','js/dataTables.min.js')
        defer = True  # Add the defer attribute          
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css','css/dataTables.min.css'),
        }      
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)         
        
        

        

        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['owner']  # You can exclude fields if needed

        widgets = {
            # 'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
        }         
        
@admin.register(Department)                             
class DepartmentAdmin(admin.ModelAdmin):   
    form = DepartmentForm  
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'   
           
    def save_model(self, request, obj, form, change):

        obj.owner = request.user if request.user.is_authenticated else None
          
        super().save_model(request, obj, form, change)      
        

            
        

          


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        exclude = ['id_no'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'date')
    form = AttendanceForm

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        exclude = ['id_no'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason', 'status')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'start_date', 'end_date')
    form = LeaveRequestForm
    
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_date', 'amount')
    list_filter = ('pay_date',)
    search_fields = ('employee__first_name', 'employee__last_name', 'pay_date')



# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publish_date')
#     list_filter = ('publish_date',)
#     search_fields = ('title', 'content')






# @admin.register(EmployeeTraining)
# class EmployeeTrainingAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'training_type', 'date', 'duration')
#     list_filter = ('training_type', 'date')
#     search_fields = ('employee__first_name', 'employee__last_name', 'training_type')

@admin.register(EmployeePromotion)
class EmployeePromotionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'promotion_date', 'previous_role', 'new_role', 'salary_change')
    list_filter = ('promotion_date', 'previous_role', 'new_role')
    search_fields = ('employee__first_name', 'employee__last_name', 'previous_role', 'new_role')

# @admin.register(TaskAssignment)
# class TaskAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'task_name', 'deadline', 'status')
#     list_filter = ('deadline', 'status')
#     search_fields = ('employee__first_name', 'employee__last_name', 'task_name')

class OvertimeRecordForm(forms.ModelForm):
    class Meta:
        model = OvertimeRecord
        exclude = ['id_no'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))

@admin.register(OvertimeRecord)
class OvertimeRecordAdmin(admin.ModelAdmin):
    list_display = ('employee',  'date', 'othour')
    list_filter = ('date',)
    search_fields = ('employee__first_name', 'employee__last_name', 'id_no')
    form = OvertimeRecordForm

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    pass

class ResignationForm(forms.ModelForm):
    class Meta:
        model = Resignation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))
@admin.register(Resignation)
class ResignationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'resignation_date', 'reason', 'notice_period', 'status')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'resignation_date')
    
    form = ResignationForm
class LeftyForm(forms.ModelForm):
    class Meta:
        model = Lefty
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))
@admin.register(Lefty)
class LeftyAdmin(admin.ModelAdmin):
    list_display = ('employee', 'left_date', 'reason',  'status')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'left_date')    
    form = LeftyForm
    