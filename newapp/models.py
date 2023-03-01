from django.db import models

# Create your models here.
class customer(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField()
    password=models.CharField(max_length=250)
    otp = models.CharField(max_length=25,default='0000')