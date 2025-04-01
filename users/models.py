from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        default='default_profile_picture.png',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
