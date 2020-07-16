from django.db import models
from django.contrib.auth.models import User

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)