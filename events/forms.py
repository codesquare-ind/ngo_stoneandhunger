from django import forms
from .models import Event, Volunteer


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'thumbnail', 'start_date', 'end_date', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title', 'required': ''}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Event Details', 'required': ''}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'required': ''},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control', 'required': ''},
                format='%Y-%m-%dT%H:%M'
            ),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location', 'required': ''}),
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = [
            'name', 'email', 'phone', 'gender', 'date_of_birth', 'education_background',
            'address', 'occupation', 'way_of_contribution', 'hours_per_day'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@mail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'education_background': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Education Background'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'way_of_contribution': forms.Select(attrs={'class': 'form-control'}),
            'hours_per_day': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hours / Day'}),

            'date_of_birth': forms.DateTimeInput(
                attrs={'type': 'date', 'class': 'form-control'},
            ),
        }
