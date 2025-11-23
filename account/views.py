from django.shortcuts import render
from django.http import JsonResponse

from .serializers import *

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def index(request):
    return JsonResponse({"message": "Account app is working!"})

# register view
class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # save user first
        user = serializer.save()

        # Generate JWT token
        tokens = user.tokens()

        return Response({
            "message": "User registered successfully!",
            "user": {
                'username': user.username,
                "id": user.id,
                'role': user.role,
            },
            "refresh": tokens['refresh_token'],
            "access": tokens['access_token']
        }, status=status.HTTP_201_CREATED)
        
# login view
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializers

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT token
        tokens = user.tokens()

        return Response({
            "message": "Login successful!",
            "user": {
                'username': user.username,
                "id": user.id,
                'role': user.role,
            },
            "refresh": tokens['refresh_token'],
            "access": tokens['access_token']
        }, status=status.HTTP_200_OK)

# logout view

# profile view


# FUTURE IMPLEMENTATIONS:
# password reset view
# update profile view
# delete account view