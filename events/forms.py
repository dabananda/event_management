from django import forms
from .models import Event, Participant, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full', 'rows': 3}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full'}),
            'description': forms.Textarea(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full'}),
            'category': forms.Select(attrs={'class': 'form-select border p-2 rounded-md shadow-sm mt-1 block w-full'}),
        }

class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox border p-2 h-4 w-4 text-indigo-600'})
    )
    
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full'}),
            'email': forms.EmailInput(attrs={'class': 'form-input border p-2 rounded-md shadow-sm mt-1 block w-full'}),
        }