#!/bin/bash

python3 src/manage.py migrate

echo "MIGRATIONS APPLIED"

cd src

gunicorn --bind 0.0.0.0:8000 config.wsgi

echo "RUNNING WEB"
