#!/bin/bash
set -e

echo "BUILD START"

pip install -r requirements.txt

echo "Applying database migrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "BUILD END"
