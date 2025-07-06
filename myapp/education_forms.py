from django import forms
from .models import EducationPage

class EducationPageUploadForm(forms.ModelForm):
    upload = forms.ImageField(required=False, label="上傳圖片（可選）")

    class Meta:
        model = EducationPage
        fields = ['title', 'url']

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get('upload')

        if upload:
            instance.image_url = upload.read()  # 讀取圖片的二進位內容

        if commit:
            instance.save()
        return instance
