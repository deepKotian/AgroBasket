from django.db import models
from autoslug import AutoSlugField

class Register(models.Model):
    name = models.CharField(max_length=255),
    password = models.CharField(max_length= 20),
    email = models.CharField(max_length=255)

class FarmerProfile(models.Model):
    pass

class FarmerProduct(models.Model):
    prodID = models.AutoField(primary_key=True)
    compName =  models.CharField(max_length=255)
    prodName = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/")
    price = models.IntegerField(default=0)
    discPrice = models.IntegerField(default=0)
    category = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    slug =  AutoSlugField(populate_from='prodID', null=True)
    coupons = models.CharField(max_length=255)
    ratings = models.IntegerField(default=0)
    feedback = models.CharField(max_length=255)
    stockDetails = models.BooleanField(default=True)
    


