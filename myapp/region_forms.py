# regions/region_forms.py
from django import forms
from .models import TaiwanRegion

class TaiwanRegionForm(forms.ModelForm):
    class Meta:
        model = TaiwanRegion
        fields = ['zipcode', 'country_city', 'district_town']
