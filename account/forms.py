from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'pan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pan No.'}),

            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            'house_ownership': forms.Select(attrs={'class': 'form-control', 'placeholder': 'House Ownership'}),
            'rent_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rent'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
        }
