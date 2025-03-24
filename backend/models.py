from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



class Users(AbstractUser):
    email= models.EmailField(unique=True)
    user_type = models.CharField(max_length=20)
    profile_picture = models.CharField(max_length=300)
    #username = models.CharField(max_length=100,null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","password","user_type"]

    
