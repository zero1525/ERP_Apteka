from rest_framework import routers
from .jwt import MyTokenObtainPairView
from django.urls import path
from .generics import ChangePasswordView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenObtainPairView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]