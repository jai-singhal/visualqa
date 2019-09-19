from django import forms
from .models import VQAImage, Question

class ImageForm(forms.ModelForm):
    image = forms.ImageField( label='')

    class Meta:
        model = VQAImage
        exclude = ["user", "timestamp"]



