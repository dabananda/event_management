from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', default='default_profile_picture.png', blank=True)

    def __str__(self):
        return f"{self.user.user.username}'s profile"
