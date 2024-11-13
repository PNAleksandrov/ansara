from __future__ import annotations

from django.contrib import admin
from django.urls import path, include
from tracker import settings
# from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.versioning import URLPathVersioning

app_urls = [
    path('', include('app.api.urls')),
]

api_urls = [
    path('api/', include(app_urls)),
]

swagger_urls = [
    # YOUR PATTERNS
    path('schema/v1/', SpectacularAPIView.as_view(
        versioning_class=URLPathVersioning,
        api_version='v1',
        patterns=api_urls,
    ), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(template_name='drf_spectacular/swagger_ui.html'), name='spectacular-swagger-ui')
]

urlpatterns = [
    path('', include(swagger_urls)),
    path('', include(api_urls)),
    path('admin/', admin.site.urls),
]  + static(settings.STATIC_URL)