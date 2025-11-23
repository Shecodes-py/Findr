from django.urls import path
from .views import index, RegisterView, LoginView

urlpatterns = [
    path('', view=index, name='index'),
    path('register/', view=RegisterView.as_view(), name='register'),
    path('login/', view=LoginView.as_view(), name='login'),
]
