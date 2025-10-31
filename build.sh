#!/usr/bin/env bash
python -m pip install --upgrade pip
pip install -r requirements.txt

# migrate DB
python manage.py migrate --noinput

# collect static files
python manage.py collectstatic --noinput --clear
