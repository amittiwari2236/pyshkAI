from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from core.models import BaseModel

class StrictUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        if username != 'amittiwari2236':
            raise ValueError("Superuser creation is strictly limited to 'amittiwari2236'.")
        if password != 'Scholar@1910':
            raise ValueError("Invalid superuser password.")
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Staff')
    
    objects = StrictUserManager()

    def save(self, *args, **kwargs):
        if self.is_superuser and self.username != 'amittiwari2236':
            raise ValidationError("Alternative superuser credentials are not allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
