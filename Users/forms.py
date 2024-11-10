# forms.py
from django import forms
from .models import ProfileImage

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']
