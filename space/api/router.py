from rest_framework import routers
from .viewsets import SpaceViewSet, BranchViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'spaces', SpaceViewSet, basename='space')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]