# Vehicle Inventory & Booking REST API

## Project Description
A REST API for a Vehicle Inventory & Booking system. It allows managing vehicles and booking them with business logic to prevent double bookings and ensure data integrity.

## Tech Stack
- Python 3
- Django 5
- Django REST Framework
- SQLite (default)

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/a7k4a6s3h0/vechicle_inventory_booking_pr.git
   cd vehicle_system
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Copy `.env.example` to `.env` (optional, as default settings work for dev).
   ```bash
   cp .env.example .env
   ```

## Migration Commands
Run the following commands to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

## How to Run
Start the development server:
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/api/vi/`.

5. **Run Management Commands**
Run the following command to populate the database with sample data (optional):
   ```bash
   python manage.py populate_data
   ```

## API Usage

### Endpoints

#### Vehicles
- `GET /api/vi/vehicles/` - List all vehicles
- `POST /api/vi/vehicles/` - Create a new vehicle
- `GET /api/vi/vehicles/<id>/` - Retrieve vehicle details
- `PUT /api/vi/vehicles/<id>/` - Update vehicle
- `DELETE /api/vi/vehicles/<id>/` - Delete vehicle

**Filtering:**
- `/api/vi/vehicles/?brand=Toyota`
- `/api/vi/vehicles/?fuel_type=Electric`
- `/api/vi/vehicles/?is_available=true`

#### Bookings
- `GET /api/vi/bookings/` - List all bookings
- `POST /api/vi/bookings/` - Create a new booking
- `GET /api/vi/bookings/<id>/` - Retrieve booking details

### Sample JSON for Booking Creation
**POST** `/api/bookings/`

```json
{
   "vehicle": {
      "id": 1,
      "name": "Corolla",
      "brand": "Toyota",
      "year": 2022,
      "price_per_day": "50.00",
      "fuel_type": "Petrol",
      "is_available": false
   },
   "customer_name": "John Doe",
   "customer_phone": "1234567890",
   "start_date": "2023-12-01",
   "end_date": "2023-12-05",
   "total_amount": 200.00,
   "days": 4
}
```

**Note:** `total_amount` is calculated automatically based on the vehicle's price per day and the duration of the booking.

## Business Rules & Validations
- **Double Booking:** A vehicle cannot be booked if it overlaps with an existing booking.
- **Dates:** `start_date` cannot be in the past. `end_date` must be after `start_date`.
- **Phone:** `customer_phone` must be exactly 10 digits.
- **Availability:** Upon successful booking, the vehicle's `is_available` status is set to `False`.

**Api Documentation:**
[https://documenter.getpostman.com/view/24033907/2sB3dMyBkG](https://documenter.getpostman.com/view/24033907/2sB3dMyBkG)


**video demo:**
[https://drive.google.com/drive/folders/15zPrLjajBscAjqoUh9ZRH_HfZRPX6h3i?usp=sharing](https://drive.google.com/drive/folders/15zPrLjajBscAjqoUh9ZRH_HfZRPX6h3i?usp=sharing)
