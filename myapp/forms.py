from django import forms

class AutoDialForm(forms.Form):
    default_message = forms.CharField(
        label='預設訊息',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        required=False
    )
