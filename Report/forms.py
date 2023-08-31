from django import forms

class DateFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date', required=True)
    end_date = forms.DateField(label='End Date', required=True)
