from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import SellerProfile, Location
from .serializers import LocationSerializer, SellerProfileSerializer

# Create your views here.

# seller profile view
class SellerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'profile_id'

    def get_queryset(self):
        return SellerProfile.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # check if profile already exists
        if SellerProfile.objects.filter(user=request.user).exists():
            return Response({
                "message": "Seller profile already exists"
                },
                  status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor_profile = serializer.save(user=request.user)

        return Response({
                "message": "Seller profile created",
                "profile": SellerProfileSerializer(vendor_profile).data,
                },
                  status=status.HTTP_201_CREATED)   
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        vendor_profile = self.get_object()
        serializer = self.get_serializer(vendor_profile, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        vendor_profile = serializer.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'vendor_profile': SellerProfileSerializer(vendor_profile).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's seller profile"""
        try:
            seller_profile = SellerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(seller_profile)
            return Response(serializer.data)
        except SellerProfile.DoesNotExist:
            return Response({
                "message": "No seller profile found. Please create one."
            }, status=status.HTTP_404_NOT_FOUND)

class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'location_id'

    def get_queryset(self):
        # vendor_profile = SellerProfile.objects.get(user=self.request.user)
        return Location.objects.filter(vendor_profile__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            vendor_profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return Response({
                "message": "Seller profile does not exist"
                },
                  status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = serializer.save(vendor_profile=vendor_profile)
        
        return Response({
                "message": "Location created",
                "location": LocationSerializer(location).data,
                },
                  status=status.HTTP_201_CREATED)

        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            location = serializer.save()

            return Response({
                "message": "Location updated",
                "location": LocationSerializer(location).data,
                },
                  status=status.HTTP_200_OK)
        
        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            location_id = instance.location_id
            self.perform_destroy(instance)

            return Response({
                "message": "Location deleted",
                "location_id": location_id
                },
                  status=status.HTTP_200_OK)