from django import forms

class AutoDialForm(forms.Form):
    default_message = forms.CharField(
        label='預設訊息',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        required=False
    )


#-----管理員自介的
from .models import Admins

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = Admins
        fields = ['name', 'phone', 'bio']  # 不包含 email 和 password
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

#---
from .models import ThisUserProfile

class ThisUserProfileForm(forms.ModelForm):
    class Meta:
        model = ThisUserProfile
        fields = [
            "username", "gmail", "default_nickname1", "default_nickname2",
            "emergency_contact_phone", "emergency_contact_gmail",
            "default_message", "self_intro", "user_images", "status_color"
        ]
        widgets = {
            "default_message": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "self_intro": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "user_images": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "status_color": forms.TextInput(attrs={"type": "color", "class": "form-control"}),
        }