from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    
    def __str__(self):
        return self.name
    
    @property
    def is_past(self):
        event_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return event_datetime < timezone.now()
    
    @property
    def is_today(self):
        return self.date == timezone.now().date()

class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    events = models.ManyToManyField(Event, related_name='participants')
    
    def __str__(self):
        return self.name