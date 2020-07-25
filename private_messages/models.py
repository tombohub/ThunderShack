from django.db import models
from django.contrib.auth.models import User
from ads.models import Ad

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.SET_NULL, null=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)