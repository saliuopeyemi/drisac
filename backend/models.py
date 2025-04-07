from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class Users(AbstractUser):
    email= models.EmailField(unique=True)
    user_type = models.CharField(max_length=20)
    profile_picture = models.CharField(max_length=300)
    #username = models.CharField(max_length=100,null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","password","user_type"]


class Product(models.Model):
    title=models.CharField(max_length=300)
    description = models.CharField(max_length=2500)
    unit_price = models.IntegerField()

class Expenditure(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=2500)
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)


class Sales(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    revenue = models.IntegerField()
    date = models.DateField(auto_now=True)
    
