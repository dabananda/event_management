from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='events')
    rsvps = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="rsvp_events", blank=True)
    image = models.ImageField(
        upload_to='event_images/', default='default_event.jpg', blank=True, null=True)

    def __str__(self):
        return self.name
