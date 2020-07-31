from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

 # model fields, database columns
class Ad(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    phone_number =models.CharField
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='ad_images/default.png', upload_to='ad_images')

    # options of the model
    class Meta:
        ordering = ['-date_posted']

    # this is how the object to be displayed
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ad-details', kwargs={'pk':self.pk, 'slug':self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)