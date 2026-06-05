from rest_framework.viewsets import ModelViewSet
from .serializers import ReceptSerializer, ManufacturerSerializer, CategorySerializer, BarcodeSerializer
from ..models import Recepts, Manufacturer, Category, Barcode
from config.services import create_object_for_user_space

class ReceptViewsets (ModelViewSet):
    queryset = Recepts.objects.all()
    serializer_class = ReceptSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(ReceptViewsets, self.request.user, serializer.validated_data)


class ManufacturerViewsets (ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(Manufacturer, self.request.user, serializer.validated_data)

class CategoryViewsets (ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        create_object_for_user_space(Category, self.request.user, serializer.validated_data)

class BarcodeViewsets (ModelViewSet):
    queryset = Barcode.objects.all()
    serializer_class = BarcodeSerializer

    def perform_create(self, serializer):
        create_object_for_user_space(Barcode, self.request.user, serializer.validated_data)


