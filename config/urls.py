from django.contrib import admin
from django.urls import path, include 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('space/', include('space.api.router')),
    path('auth/', include('accounts.api.urls')),
    path('hr/', include('hr.api.routers')),
    path('invertory/', include('invertory.api.routers')),
    path('sales/', include('sales.api.routers')),
    path('product/', include('recepts.api.routers'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns