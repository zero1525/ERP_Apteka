from rest_framework import routers
from .jwt import MyTokenObtainPairView
from django.urls import path

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),
]