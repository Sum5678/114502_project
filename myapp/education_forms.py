from django import forms
from .models import EducationPage
import os

class EducationPageUploadForm(forms.ModelForm):
    upload = forms.ImageField(required=False, label="上傳圖片（可選）")

    class Meta:
        model = EducationPage
        fields = ['title', 'url']

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload = self.cleaned_data.get('upload')

        if upload:
            filename = upload.name
            save_path = os.path.join('myapp', 'static', 'images', filename)

            with open(save_path, 'wb+') as destination:
                for chunk in upload.chunks():
                    destination.write(chunk)

            instance.image_url = f'images/{filename}'

        if commit:
            instance.save()

        return instance
