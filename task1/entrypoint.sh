#!/bin/bash

echo "Running database migrations..."
flask db upgrade  # Applies migrations

echo "Starting the application..."
exec gunicorn -b 0.0.0.0:8000 "app:create_app()"
