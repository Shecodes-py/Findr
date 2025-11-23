from django.urls import path, include
from .views import SellerProfileViewSet, LocationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vendor-profile', SellerProfileViewSet, basename='vendor-profile')
router.register(r'location', LocationViewSet, basename='location')

urlpatterns = [
    path('', include(router.urls)),
]