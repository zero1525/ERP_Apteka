from rest_framework.routers import DefaultRouter
from .viwsets import StockViewSet, SupplierViewSet, InventoryDocumentViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register(r'stock', StockViewSet, basename= 'stock')
router.register(r'suplier', SupplierViewSet, basename = 'suplier')
router.register(r'invertorydokument', InventoryDocumentViewSet, basename='invertorydokument')
router.register(r'invertoryitem', InventoryItemViewSet, basename='invertoryitem')


urlpatterns = router.urls