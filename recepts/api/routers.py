from rest_framework import routers
from .viewsets import ReceptViewsets, ManufacturerViewsets, CategoryViewsets, BarcodeViewsets

router = routers.DefaultRouter()
router.register(r'recepts', ReceptViewsets, basename='recepts'),
router.register(r'manufacturers', ManufacturerViewsets, basename='manufacturers'),
router.register(r'categories', CategoryViewsets, basename='categories'),
router.register(r'barcodes', BarcodeViewsets, basename='barcodes')

urlpatterns = router.urls