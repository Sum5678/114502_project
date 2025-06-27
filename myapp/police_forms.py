from django import forms
from .models import PoliceAddress

class PoliceAddressForm(forms.ModelForm):
    class Meta:
        model = PoliceAddress
        fields = '__all__'
