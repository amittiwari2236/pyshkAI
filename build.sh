#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create a default superuser (since Render Free tier has no Shell)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"
