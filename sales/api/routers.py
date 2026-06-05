from rest_framework.routers import DefaultRouter
from .viewsets import ChecItemViewSets, HeaderCheckViewSets

router = DefaultRouter()
router.register(r'checitem', ChecItemViewSets, basename='checitem'),
router.register(r'headercheck', HeaderCheckViewSets, basename='headercheck')

urlpatterns = router.urls