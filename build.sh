#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create a default superuser (since Render Free tier has no Shell)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='amittiwari2236').exists() or User.objects.create_superuser('amittiwari2236', 'amittiwari2236@example.com', 'admin123')"
