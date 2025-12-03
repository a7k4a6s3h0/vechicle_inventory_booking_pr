from rest_framework import serializers
from .models import Vehicle, Booking
from datetime import date

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
    
    def validate(self, data):
        errors = {}
        price = data.get('price_per_day')
        name = data.get('name')
        brand = data.get('brand')

        if price is not None and price < 0:
            errors['price_per_day'] = "Price per day cannot be negative."

        name = name or (self.instance.name if self.instance else None)
        brand = brand or (self.instance.brand if self.instance else None)

        if name and brand:
            queryset = Vehicle.objects.filter(name=name, brand=brand)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                errors['vehicle'] = "Vehicle with this name and brand already exists."
        
        if errors:
            raise serializers.ValidationError(errors)

        return data
    

class BookingSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        write_only=True,
        source='vehicle'
    )
    days = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['id', 'vehicle', 'vehicle_id', 'customer_name', 'customer_phone', 'start_date', 'end_date', 'total_amount', 'days']
        read_only_fields = ['total_amount', 'days']

    def get_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None
    
    def validate_customer_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Customer phone must be exactly 10 digits.")
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        vehicle = data.get('vehicle')

        # 1. start_date cannot be in the past
        if start_date < date.today():
            raise serializers.ValidationError("Start date cannot be in the past.")

        # 2. end_date must be after start_date
        if end_date <= start_date:
            raise serializers.ValidationError("End date must be after start_date.")

        # 3. Vehicle cannot be double-booked
        overlapping_bookings = Booking.objects.filter(
            vehicle=vehicle,
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        if self.instance:
            overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Vehicle is already booked for the selected dates.")

        return data

    def create(self, validated_data):
        vehicle = validated_data['vehicle']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        # 1. Calculate total_amount
        days = (end_date - start_date).days
        total_amount = days * vehicle.price_per_day
        validated_data['total_amount'] = total_amount

        # 2. Update vehicle availability
        vehicle.is_available = False
        vehicle.save()

        return super().create(validated_data)
