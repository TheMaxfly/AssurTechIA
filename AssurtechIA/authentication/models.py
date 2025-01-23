from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    Admin = "admin"
    Customer = "customer"

    ROLE_CHOICES = (
        (Admin, "Admin"),
        (Customer, "Customer"),
    )


    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=30, 
        choices=ROLE_CHOICES, 
        verbose_name='Rôle', 
        default=Customer
    )

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = [] 

    objects = UserManager()

    def __str__(self):
        return self.email