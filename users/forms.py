from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
