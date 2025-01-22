from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):


    Admin = "admin"
    Customer = "customer"

ROLE_CHOICES = (
    (User.Admin, "Admin"),
    (User.Customer, "Customer"),
)

role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')



# Create your models here.
