from django import forms
from .models import TaiwanRegion

class TaiwanRegionForm(forms.ModelForm):
    class Meta:
        model = TaiwanRegion
        fields = ['zipcode', 'country_city', 'district_town']
        widgets = {
            'zipcode': forms.TextInput(attrs={
                'placeholder': '郵遞區號',
                'class': 'form-control',
            }),
            'country_city': forms.TextInput(attrs={
                'placeholder': '縣市',
                'class': 'form-control',
            }),
            'district_town': forms.TextInput(attrs={
                'placeholder': '鄉鎮市區',
                'class': 'form-control',
            }),
        }
