from rest_framework import serializers
from .models import SellerProfile, Location

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['profile_id', 'user', 'store_name', 'description', 'phone_number', 'created_at', 'updated_at']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'vendor_profile', 'address_line1', 'city', 'latitude', 'longitude', 'state', 'postal_code', 'country', 'created_at', 'updated_at']