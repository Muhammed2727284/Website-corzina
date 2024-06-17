from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DolgViewSet

router = DefaultRouter()
router.register(r'dolgs', DolgViewSet)

urlpatterns = [
    path('', include(router.urls)),
]