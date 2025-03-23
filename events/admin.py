from django.contrib import admin
from events.models import Event, Category

admin.site.register(Event)
admin.site.register(Category)