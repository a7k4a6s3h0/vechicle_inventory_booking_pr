from django.core.management.base import BaseCommand
from inventory.models import Vehicle, Booking
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating vehicles...')
        
        vehicles_data = [
            {
                "name": "Corolla",
                "brand": "Toyota",
                "year": 2022,
                "price_per_day": 50.00,
                "fuel_type": "Petrol",
                "is_available": True
            },
            {
                "name": "Civic",
                "brand": "Honda",
                "year": 2023,
                "price_per_day": 55.00,
                "fuel_type": "Petrol",
                "is_available": True
            },
            {
                "name": "Model 3",
                "brand": "Tesla",
                "year": 2023,
                "price_per_day": 120.00,
                "fuel_type": "Electric",
                "is_available": True
            },
            {
                "name": "Mustang",
                "brand": "Ford",
                "year": 2021,
                "price_per_day": 90.00,
                "fuel_type": "Petrol",
                "is_available": True
            },
            {
                "name": "X5",
                "brand": "BMW",
                "year": 2022,
                "price_per_day": 150.00,
                "fuel_type": "Diesel",
                "is_available": True
            }
        ]

        created_vehicles = []
        for v_data in vehicles_data:
            vehicle, created = Vehicle.objects.get_or_create(
                name=v_data['name'],
                brand=v_data['brand'],
                defaults=v_data
            )
            created_vehicles.append(vehicle)
            if created:
                self.stdout.write(f'Created vehicle: {vehicle}')
            else:
                self.stdout.write(f'Vehicle already exists: {vehicle}')

        self.stdout.write('Creating bookings...')
        
        # Booking 1: Past booking (completed)
        booking1_start = date.today() - timedelta(days=10)
        booking1_end = date.today() - timedelta(days=5)
        Booking.objects.get_or_create(
            vehicle=created_vehicles[0],
            customer_name="John Doe",
            customer_phone="1234567890",
            start_date=booking1_start,
            end_date=booking1_end,
            total_amount=5 * created_vehicles[0].price_per_day
        )
        # created_vehicles[0].is_available = False
        # created_vehicles[0].save()
        
        # Booking 2: Future booking
        booking2_start = date.today() + timedelta(days=5)
        booking2_end = date.today() + timedelta(days=10)
        Booking.objects.get_or_create(
            vehicle=created_vehicles[1],
            customer_name="Jane Smith",
            customer_phone="0987654321",
            start_date=booking2_start,
            end_date=booking2_end,
            total_amount=5 * created_vehicles[1].price_per_day
        )
        created_vehicles[1].is_available = False
        created_vehicles[1].save()
        
        # Booking 3: Active booking
        booking3_start = date.today() - timedelta(days=1)
        booking3_end = date.today() + timedelta(days=2)
        Booking.objects.get_or_create(
            vehicle=created_vehicles[2],
            customer_name="Active User",
            customer_phone="1122334455",
            start_date=booking3_start,
            end_date=booking3_end,
            total_amount=3 * created_vehicles[2].price_per_day
        )
        created_vehicles[2].is_available = False
        created_vehicles[2].save()
        self.stdout.write(f'Created active booking for {created_vehicles[2]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated dummy data'))
