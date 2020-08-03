from django import forms
from .models import PrivateMessage


## for use in ad-details
class PrivateMessageForm(forms.ModelForm):
    body =  forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Or write a message...', 'rows':4, 'id':'ad-reply'}), label='')
    class Meta:
        model = PrivateMessage
        fields = ['body']

## for use inside conversations messaging
class ConversationMessageForm(forms.ModelForm):
    body =  forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder':'Type message...', 'id':'message-input'}))
    class Meta:
        model = PrivateMessage
        fields = ['body']

        