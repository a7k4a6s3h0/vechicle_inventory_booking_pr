from django.test import TestCase
from .models import Vehicle, Booking
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status

class BookingTests(TestCase):
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

    def test_create_booking_success(self):
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        data = {
            "vehicle": self.vehicle.id,
            "customer_name": "Alice",
            "customer_phone": "1234567890",
            "start_date": start_date,
            "end_date": end_date
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.vehicle.refresh_from_db()
        self.assertFalse(self.vehicle.is_available)
        booking = Booking.objects.first()
        self.assertEqual(booking.total_amount, 300.00)

    def test_create_booking_overlap(self):
        # Create initial booking
        start_date = date.today() + timedelta(days=1)
        end_date = start_date + timedelta(days=3)
        Booking.objects.create(
            vehicle=self.vehicle,
            customer_name="Bob",
            customer_phone="1234567890",
            start_date=start_date,
            end_date=end_date,
            total_amount=300.00
        )
        
        # Try to book overlapping dates
        data = {
            "vehicle": self.vehicle.id,
            "customer_name": "Charlie",
            "customer_phone": "0987654321",
            "start_date": start_date + timedelta(days=1),
            "end_date": end_date + timedelta(days=1)
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Vehicle is already booked", str(response.data))

    def test_past_date_booking(self):
        start_date = date.today() - timedelta(days=5)
        end_date = start_date + timedelta(days=3)
        data = {
            "vehicle": self.vehicle.id,
            "customer_name": "Dave",
            "customer_phone": "1234567890",
            "start_date": start_date,
            "end_date": end_date
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Start date cannot be in the past", str(response.data))
