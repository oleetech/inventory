from django import forms
from .models import Employee,Attendance

class EmployeeSelectForm(forms.Form):
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
    
class AttendanceUploadForm(forms.Form):
    text_file = forms.FileField()   
class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=True,)
    end_date = forms.DateField(label='End Date', required=True)
    
    def __init__(self, *args, **kwargs):
        super(DateFilterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })   
class YearFilterForm(forms.Form):
    year = forms.IntegerField(label='Year', required=True,)

    
    def __init__(self, *args, **kwargs):
        super(YearFilterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })               
                
            
class EmployeeIDDateFilterForm(forms.Form):
    id_no = forms.CharField(max_length=20, label='Employee ID')
    start_date = forms.DateField(label='Start Date', required=True,)
    end_date = forms.DateField(label='End Date', required=True)    
    def __init__(self, *args, **kwargs):
        super(EmployeeIDDateFilterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })    
            





   
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            