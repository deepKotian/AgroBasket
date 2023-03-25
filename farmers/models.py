from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=255),
    password = models.CharField(max_length= 20),
    email = models.CharField(max_length=255)
