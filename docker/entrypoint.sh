#!/bin/bash

python3 src/manage.py migrate

echo "MIGRATIONS APPLIED"

python3 src/manage.py runserver 0.0.0.0:8000

echo "RUNNING WEB"
