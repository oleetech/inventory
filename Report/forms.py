from django import forms

from GeneralSettings.models import Department
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


class OrderFilterForm(forms.Form):
    orderNo = forms.IntegerField(label='Order No', required=True,)

    
    def __init__(self, *args, **kwargs):
        super(OrderFilterForm, self).__init__(*args, **kwargs)
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
            
             
            
class DepartmentYearFilter(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Select a Department",
        empty_label="All Departments",
    )
    year = forms.IntegerField(
        label="Enter a Year",
        min_value=1900,  # Adjust this to your desired minimum year
        max_value=2099,  # Adjust this to your desired maximum year
        required=False,  # Make it optional
    )            
    def __init__(self, *args, **kwargs):
        super(DepartmentYearFilter, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })       
            
            
            
class DateDepartmentFilter(forms.Form):

    start_date = forms.DateField(label='Start Date', required=True,)
    end_date = forms.DateField(label='End Date', required=True)
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Select a Department",
        empty_label="All Departments",
    )
                
    def __init__(self, *args, **kwargs):
        super(DateDepartmentFilter, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            }) 
              
class OrderDepartmentFilter(forms.Form):
    orderNo = forms.IntegerField(label='Order No', required=True,)

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="Select a Department",
        empty_label="All Departments",
    )
                
    def __init__(self, *args, **kwargs):
        super(OrderDepartmentFilter, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })
            
            
            
from Sales.models import SalesEmployee

class SalesEmployeeForm(forms.Form):
    sales_employee = forms.ModelChoiceField(queryset=SalesEmployee.objects.all(), empty_label=None)                                       