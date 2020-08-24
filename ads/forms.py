from django import forms
from .models import Ad


class AdCreateForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['title', 'price', 'description', 'image']
