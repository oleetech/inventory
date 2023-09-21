from django import forms

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()
    
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
class Personal_Details(forms.Form):
    photo = forms.ImageField(label='Photo')
    name = forms.CharField(max_length=100, label='Name')
    fatherName = forms.CharField(max_length=100, label="Father's Name")
    dateofBirth = forms.DateField(label='Date of Birth')
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender')
    
    phone = forms.CharField(max_length=15, label='Phone Number')
    localAddress = forms.CharField(max_length=200, label='Local Address')
    permanentAddress = forms.CharField(max_length=200, label='Permanent Address')
    
    def __init__(self, *args, **kwargs):
        super(Personal_Details, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            }) 
            
class CompanyDetailsForm(forms.Form):
    employeeID = forms.CharField(max_length=20, label='Employee ID')
    department = forms.CharField(max_length=100, label='Department')
    designation = forms.CharField(max_length=100, label='Designation')
    joiningDate = forms.DateField(label='Joining Date')
    joiningSalary = forms.DecimalField(max_digits=10, decimal_places=2, label='Joining Salary')            


    def __init__(self, *args, **kwargs):
        super(CompanyDetailsForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-sm',
                'id': f"{field_name}",
            })                  