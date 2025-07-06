from django import forms

class AutoDialForm(forms.Form):
    default_message = forms.CharField(
        label='預設訊息',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        required=False
    )


#-----管理員自介的
from django import forms
from .models import Admins

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admins
        fields = ['name', 'phone', 'bio']  # 不包含 email 和 password
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
