from django.forms import ModelForm
from .models import PrivateMessage

class PrivateMessageForm(ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['body']