from django.test import TestCase
from .models import Vehicle, Booking
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status

class VehicleUpdateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vehicle = Vehicle.objects.create(
            name="Camry",
            brand="Toyota",
            year=2022,
            price_per_day=100.00,
            fuel_type="Hybrid",
            is_available=True
        )

    def test_update_vehicle_success(self):
        data = {
            "name": "Camry Updated",
            "brand": "Toyota",
            "year": 2022,
            "price_per_day": 110.00,
            "fuel_type": "Hybrid",
            "is_available": True
        }
        response = self.client.put(f'/api/v1/vehicles/{self.vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.name, "Camry Updated")
        self.assertEqual(self.vehicle.price_per_day, 110.00)

    def test_update_vehicle_duplicate_fail(self):
        Vehicle.objects.create(
            name="Civic",
            brand="Honda",
            year=2023,
            price_per_day=55.00,
            fuel_type="Petrol"
        )
        data = {
            "name": "Civic",
            "brand": "Honda",
            "year": 2022,
            "price_per_day": 110.00,
            "fuel_type": "Hybrid",
            "is_available": True
        }
        response = self.client.put(f'/api/v1/vehicles/{self.vehicle.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Vehicle with this name and brand already exists", str(response.data))

class BookingDeleteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vehicle = Vehicle.objects.create(
            name="Accord",
            brand="Honda",
            year=2022,
            price_per_day=100.00,
            fuel_type="Hybrid"
        )
        self.booking = Booking.objects.create(
            vehicle=self.vehicle,
            customer_name="John",
            customer_phone="1234567890",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            total_amount=200.00
        )

    def test_delete_booking(self):
        response = self.client.delete(f'/api/v1/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)
