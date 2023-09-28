from django.contrib import admin
from .models import Employee,Department,Attendance, LeaveRequest, Payroll,PayrollItem,  Announcement,EmployeeTraining, EmployeePromotion, TaskAssignment,OvertimeRecord,Holiday,Resignation,Lefty,Shift,EmployeeDocument,EmployeeLoan, LoanRepayment
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
    
    
    
class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = '__all__'


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_time', 'end_time')
    search_fields = ('name', 'start_time', 'end_time')

    form = ShiftForm
    
@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'document_name', 'document_type', 'upload_date')
    list_filter = ('document_type', 'upload_date')
    search_fields = ('employee__first_name', 'document_name')  
    
@admin.register(EmployeeLoan)    
class EmployeeLoanAdmin(admin.ModelAdmin):
    list_display = ('employee', 'loan_type', 'loan_amount', 'get_due_amount','is_complete')
    list_filter = ('loan_type', 'start_date', 'end_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name', 'loan_type')

    def get_due_amount(self, obj):
        return obj.get_due_amount()

    get_due_amount.short_description = 'Due Amount'
@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'repayment_amount', 'repayment_date', 'get_received_amount')
    list_filter = ('repayment_date',)
    search_fields = ('loan__employee__user__first_name', 'loan__employee__user__last_name')

    def get_received_amount(self, obj):
        return obj.loan.loan_amount - obj.loan.get_due_amount()

    get_received_amount.short_description = 'Received Amount'      
    
    
    
class PayrollItemAdminForm(forms.ModelForm):
    class Meta:
        model = PayrollItem
        exclude = ['id_no','department','created','docNo'] 
class PayrollItemInline(admin.TabularInline):
    model = PayrollItem
    form = PayrollItemAdminForm
    extra = 0            
    
    def save(self, *args, **kwargs):
        # Set the id_no field to the employee's id_no
        if not self.id_no:
            self.id_no = self.employee.id_no
            
        if not self.department:
            self.department = self.payroll.department     
            
        if not self.created:
            self.created = self.payroll.created    
        if not self.docNo:
            self.docNo = self.payroll.docNo                               
        super().save(*args, **kwargs)    
    class Meta:
        unique_together = ('created', 'employee')   
            
class PayrollAdminForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            last_quotation = Payroll.objects.order_by('-docNo').first()
            if last_quotation:
                next_quotation_number = last_quotation.docNo + 1
            else:
                next_quotation_number = 1

            self.initial['docNo'] = next_quotation_number    
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    form = PayrollAdminForm
    inlines = [PayrollItemInline]
    change_form_template = 'admin/Production/ProductionOrder/change_form.html'         
    class Media:
        js = ('js/payroll.js',)
        defer = True
        css = {
            'all': ('css/bootstrap.min.css','css/admin_styles.css'),
        }     
    
    