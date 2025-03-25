from events.models import Category, Event
from django import forms
from events.models import Category
from events.mixins import TailwindFormMixin


class CategoryForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={}),
        }


class EventForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date',
                  'time', 'location', 'category', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
