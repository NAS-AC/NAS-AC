#!/bin/bash
set -e

echo "Reading properties.yaml"
mv ./temp/properties.yaml /data

#TODO: replace Sqlite with the actual database name
echo "Migrating into Sqlite"
python manage.py makemigrations
python manage.py makemigrations core

python manage.py migrate
python manage.py migrate core

echo "Starting the application..."
exec python manage.py runserver 0.0.0.0:8000
