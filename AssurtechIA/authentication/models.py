from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator


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
    

    

class Prediction (models.Model):  



    class Genre (models.TextChoices):
       homme = 'homme'  
       femme = 'femme'

    genre=models.fields.CharField(choices=Genre.choices,max_length=10)
    
    is_smoker=bool

    class Region (models.TextChoices):

        southwest = 'sud-ouest'
        northwest = 'nord-ouest'
        southeast =  'sud-est'
        northeast = 'nord-est'

    region= models.fields.CharField(choices=Region.choices,max_length=10)

    age = models.fields.IntegerField(validators=[MinValueValidator(16),MaxValueValidator(100)]) 

    weight = models.fields.IntegerField(validators=[MinValueValidator(20),MaxValueValidator(450)]) 

    size = models.fields.IntegerField(validators=[MinValueValidator(100),MaxValueValidator(260)]) 

    bmi = models.fields.FloatField

    number_children = models.fields.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)]) 

    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

