from django.db import models
from vendors.models import Location, SellerProfile


# Create your models here.

class Product(models.Model):
    vendor = models.ForeignKey(SellerProfile,null=True, blank=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    product_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(blank=True, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'products'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image_url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)
    public_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"