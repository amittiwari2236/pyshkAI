from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_superuser(sender, **kwargs):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='amittiwari2236').exists():
        User.objects.create_superuser('amittiwari2236', password='Scholar@1910')

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        post_migrate.connect(create_superuser, sender=self)
