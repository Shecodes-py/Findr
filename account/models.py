from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'), 
        ('seller', 'Seller'),
    )

    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
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
    
class UserProfile(models.Model):
    id = models.ForeignKey(CustomUser.id, on_delete=models.CASCADE, related_name='')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=30, choices=CustomUser.ROLE_CHOICES, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    owner_id = models.ForeignKey(UserProfile.id, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=255, null=False, blank=False)
    category_id = models.ForeignKey(Category.id, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Business_views(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    business_id = models.ForeignKey(Business.id, on_delete=models.CASCADE, related_name='views')
    user_id = models.ForeignKey(Business.id, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)
    # view_count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.business.name} - {self.view_count} views"

class SavedBusiness(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    business_id = models.ForeignKey(Business.id, on_delete=models.CASCADE, related_name='saved_by', unique=True)
    user_id = models.ForeignKey(CustomUser.id, on_delete=models.CASCADE, related_name='saved_businesses', unique=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} saved {self.business.name}"
    
class Orders(models.Model):
    STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('accepted', 'Processing'),
        ('completed', 'Shipped'),
        ('cancelled', 'Cancelled'),
    }
    
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    order_number = models.IntegerField(max_length=100, unique=True)

    user_id = models.ForeignKey(UserProfile.id, on_delete=models.CASCADE, related_name='orders')
    business_id = models.ForeignKey(Business.id, on_delete=models.CASCADE, related_name='orders')
    seller_id = models.ForeignKey(UserProfile.id, on_delete=models.CASCADE, related_name='seller_orders')
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    order_note = models.CharField(max_length=255, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.buyer.username} from {self.business.name}"
    
    class Meta:
        ordering = ['-order_number']

class SearchLogs(models.Model):
    id = models.UUIDField(primary_key=True, default=models.UUIDField, editable=False)
    user_id = models.ForeignKey(CustomUser.id, on_delete=models.CASCADE, related_name='search_logs')
    raw_query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    detected_category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} searched for '{self.query}'"