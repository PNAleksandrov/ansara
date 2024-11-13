from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path('v1/tasks/', include('app.api.v1.urls')),
]