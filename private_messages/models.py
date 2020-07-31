from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from ads.models import Ad

class Conversation(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='starter', on_delete=models.SET_NULL, null=True)
    participant = models.ForeignKey(User, related_name='participant', on_delete=models.SET_NULL, null=True)
    

    def get_absolute_url(self):
        return reverse('messages-conversation', kwargs={'pk':self.pk})

    @classmethod
    def get_if_exists(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return "multiple"

    def latest_message(self):
        try:
            return self.privatemessage_set.order_by('-id')[0]
        except IndexError:
            return None


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    conversation =  models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)

