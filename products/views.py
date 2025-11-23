from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response   

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer 

# Create your views here.

# product viewawt
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'product_id'

    def create(self, request, *args, **kwargs):
        # Logic to create a product
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({
            "message": "Product created",
            "product": product.product_id,
            },
              status=status.HTTP_201_CREATED
    )

    def update(self, request, *args, **kwargs):
        # Logic to update a product
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response({
            "message": "Product updated",
            "product": product.product_id,
            },
              status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        # Logic to delete a product
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Product deleted",
            },
              status=status.HTTP_200_OK)
    
    