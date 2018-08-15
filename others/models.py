from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    skype = models.CharField(max_length=30, null=True, blank=True)
    businesshour = models.CharField(max_length=50, blank=True)
