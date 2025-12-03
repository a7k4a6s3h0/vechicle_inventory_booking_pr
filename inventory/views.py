from rest_framework import viewsets
from .models import Vehicle, Booking
from .serializers import VehicleSerializer, BookingSerializer
from rest_framework.response import Response
from rest_framework import status

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        brand = self.request.query_params.get('brand')
        fuel_type = self.request.query_params.get('fuel_type')
        is_available = self.request.query_params.get('is_available')

        if brand:
            queryset = queryset.filter(brand__iexact=brand)
        if fuel_type:
            queryset = queryset.filter(fuel_type__iexact=fuel_type)
        if is_available is not None:
            if is_available.lower() == 'true':
                queryset = queryset.filter(is_available=True)
            elif is_available.lower() == 'false':
                queryset = queryset.filter(is_available=False)
        
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Vehicle deleted successfully."},
            status=status.HTTP_200_OK
        )

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        vehicle = instance.vehicle
        self.perform_destroy(instance)
        if not Booking.objects.filter(vehicle=vehicle).exists():
            vehicle.is_available = True
            vehicle.save()
        return Response(
            {"detail": "Booking deleted successfully."},
            status=status.HTTP_200_OK
        )