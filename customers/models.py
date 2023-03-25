import uuid
from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.
class CompleteProfile(models.Model):
    username = models.CharField(max_length=255, default="")
    fullName = models.CharField(max_length=255)
    emailAddress = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    
class Products(models.Model):
    comp_name = models.CharField(max_length=255)
    product_id = models.AutoField
    image = models.ImageField(upload_to="images/", null=True)
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    price = models.CharField(max_length=250)
    discounted_price = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    slug =  AutoSlugField(populate_from='name', null=True)
    ratings = models.CharField(max_length=255)
    stock_status = models.CharField(max_length=255)

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    completed = models.BooleanField(default=False)

    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([float(item.get_total) for item in cartitems])
        return total
    
    @property
    def get_itemtotal(self):
        cartitems = self.cartitems_set.all()
        total = sum([float(item.quantity) for item in cartitems])
        return total

    def __str__(self):
        return str(self.id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product =  models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total(self):
        total = float(self.quantity) * float(self.product.price)
        if total == 0.00:
            self.delete()
        return total

    def __str__(self):
        return self.product.name

