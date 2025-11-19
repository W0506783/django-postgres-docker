# events/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegistrationViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'registrations', RegistrationViewSet, basename='registration')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]