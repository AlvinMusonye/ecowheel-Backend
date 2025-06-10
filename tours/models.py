from django.db import models
from cloudinary.models import CloudinaryField

class Tour(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField("image", blank=True, null=True)
    category = models.CharField(max_length=100)

   

    def __str__(self):
        return self.title
