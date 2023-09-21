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