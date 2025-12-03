from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
