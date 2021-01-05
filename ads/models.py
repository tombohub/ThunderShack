from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image
from django.core.files import File
from io import BytesIO
import os

# Create your models here.

# model fields, database columns


class Ad(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    phone_number = models.CharField
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='ad_images/default.png', upload_to='ad_images')
    thumbnail = models.ImageField(
        default='ad_thumbnails/default.png', upload_to='ad_thumbnails')

    # options of the model
    class Meta:
        ordering = ['-date_posted']

    # this is how the object to be displayed
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad-details', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # first save so we can have images saved in database. its simpler
        super().save(*args, **kwargs)

        ## Handle the uploaded images.
        img = Image.open(self.image)
        output_io = BytesIO()
        name = os.path.basename(self.image.name)

        # Make a thumbnail
        thumbnail_size = (500, 500)
        img_copy = img.copy()
        img_copy.thumbnail(thumbnail_size, Image.ANTIALIAS)
        img_copy.save(output_io, 'JPEG', quality=90, subsampling=0)
        
        # save=False in order not to call super().save() again and again..
        self.thumbnail.save(name, File(output_io), save=False)


        # Resize the original image
        output_width = 1000
        width_percent = (output_width/float(img.size[0]))
        output_height = int((float(img.size[1])*float(width_percent)))
        img = img.resize((output_width,output_height), Image.ANTIALIAS)
        img.save(output_io, 'JPEG', quality=90, subsampling=0)
        
        # save=False in order not to call super().save() again and again..
        self.image.save(name, File(output_io), save=False)
        
        
        super().save(*args, **kwargs)
