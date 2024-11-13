from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api.v1.views import TaskListCreateView, TaskCreateAPIView, TaskDestroy

urlpatterns = [
    path('list/', TaskListCreateView.as_view()),
    path('create/', TaskCreateAPIView.as_view()),
    path('delete/<int:pk>/', TaskDestroy.as_view())
]