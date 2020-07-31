from django import forms
from .models import PrivateMessage

class PrivateMessageForm(forms.ModelForm):
    body =  forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Or write a message...', 'rows':4}), label='')
    class Meta:
        model = PrivateMessage
        fields = ['body']