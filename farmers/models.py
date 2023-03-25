from django.db import models
from autoslug import AutoSlugField

class Register(models.Model):
    name = models.CharField(max_length=255),
    password = models.CharField(max_length= 20),
    email = models.CharField(max_length=255)

class FarmerProfile(models.Model):
    username = models.CharField(max_length=255, default="")
    fullName = models.CharField(max_length=255, default="")
    emailAddress = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=255, default="")
    city = models.CharField(max_length=255, default="")
    state = models.CharField(max_length=255, default="")
    zipcode = models.CharField(max_length=255, default="")
    comp_name = models.CharField(max_length=255, default="")



