from django.contrib import admin
from .models import Employee,EmployeeSkill,Department,Skill,District, PoliceStation,Attendance, LeaveRequest, Payroll, Document, Announcement,EmployeeTraining, EmployeePromotion, TaskAssignment,AttendanceLog,OvertimeRecord
from django import forms
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Register your models here.
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['owner','district','police_station']  # You can exclude fields if needed

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
        
        
# class EmployeeSkillForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeSkill
#         exclude = ['owner']  # You can exclude fields if needed

       
        
# @admin.register(EmployeeSkill)                             
# class EmployeeSkillAdmin(admin.ModelAdmin):   
#     form = EmployeeForm  
#     change_form_template = 'admin/Production/ProductionOrder/change_form.html'   
           
#     def save_model(self, request, obj, form, change):

#         obj.owner = request.user if request.user.is_authenticated else None
          
#         super().save_model(request, obj, form, change)      
        
        
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
        
# class SkillForm(forms.ModelForm):
#     class Meta:
#         model = Skill
#         exclude = ['owner']  # You can exclude fields if needed

#         widgets = {
#             # 'name': forms.TextInput(attrs={'readonly': 'readonly'}),
 
#         }         
        
# @admin.register(Skill)                             
# class SkillAdmin(admin.ModelAdmin):   
#     form = SkillForm  
#     change_form_template = 'admin/Production/ProductionOrder/change_form.html'   
           
#     def save_model(self, request, obj, form, change):

#         obj.owner = request.user if request.user.is_authenticated else None
          
#         super().save_model(request, obj, form, change)                
        

          
# class PoliceStationInline(admin.TabularInline):  # or admin.StackedInline
#     model = PoliceStation
#     extra = 0
 
           
# @admin.register(District)
# class DistrictAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     inlines = [PoliceStationInline]        

# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Attendance
#         exclude = ['id_no'] 

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['employee'].widget = forms.Select(choices=Employee.objects.values_list('id', 'id_no'))

# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'date', 'status')
#     list_filter = ('date', 'status')
#     search_fields = ('employee__first_name', 'employee__last_name', 'date')
#     form = AttendanceForm

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'reason', 'status')
    list_filter = ('status',)
    search_fields = ('employee__first_name', 'employee__last_name', 'start_date', 'end_date')

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_date', 'amount')
    list_filter = ('pay_date',)
    search_fields = ('employee__first_name', 'employee__last_name', 'pay_date')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_type', 'upload_date')
    list_filter = ('document_type', 'upload_date')
    search_fields = ('employee__first_name', 'employee__last_name', 'document_type')

# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = ('title', 'publish_date')
#     list_filter = ('publish_date',)
#     search_fields = ('title', 'content')






@admin.register(EmployeeTraining)
class EmployeeTrainingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training_type', 'date', 'duration')
    list_filter = ('training_type', 'date')
    search_fields = ('employee__first_name', 'employee__last_name', 'training_type')

@admin.register(EmployeePromotion)
class EmployeePromotionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'promotion_date', 'previous_role', 'new_role', 'salary_change')
    list_filter = ('promotion_date', 'previous_role', 'new_role')
    search_fields = ('employee__first_name', 'employee__last_name', 'previous_role', 'new_role')

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task_name', 'deadline', 'status')
    list_filter = ('deadline', 'status')
    search_fields = ('employee__first_name', 'employee__last_name', 'task_name')

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    pass

@admin.register(OvertimeRecord)
class OvertimeRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'id_no', 'date', 'ot_hour')
    list_filter = ('date',)
    search_fields = ('employee__first_name', 'employee__last_name', 'id_no')
