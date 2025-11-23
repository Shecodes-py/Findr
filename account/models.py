from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'), 
        ('seller', 'Seller'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=False) 
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        # attaching custom claims
        refresh['role'] = self.role

        return{
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token)
        }