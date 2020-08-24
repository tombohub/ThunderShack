from django import forms
from .models import Ad


class AdCreateForm(forms.ModelForm):
    image = forms.ImageField()
    image.widget.attrs.update({'capture': ''})

    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image']
