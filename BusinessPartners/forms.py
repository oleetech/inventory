from django import forms
from .models import BusinessPartner

class CustomBusinessPartnerForm(forms.ModelForm):
    class Meta:
        model = BusinessPartner
        fields = '__all__'  # সব ফিল্ড অবশ্যই যোগ করুন

    # যেহেতু BusinessPartner মডেলে currency_type এবং vendor_type ফিল্ডের একটি choices ফিল্ড আছে, আমি এটি একটি রেডিও বাটন রুপে দেখাতে চাই
    currency_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BusinessPartner.CURRENCY_TYPES)
    vendor_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BusinessPartner.VENDOR_TYPES)
