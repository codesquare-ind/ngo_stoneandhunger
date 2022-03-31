from django.db import models
from ckeditor.fields import RichTextField


class Event(models.Model):
    thumbnail = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True)
    description = RichTextField(null=True)
    start_date = models.DateTimeField(auto_now_add=False, null=True)
    end_date = models.DateTimeField(auto_now_add=False, null=True)
    location = models.CharField(max_length=250, null=True)


class Volunteer(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    CONTRIBUTE = (
        ('From Home', 'Volunteer From Home'),
        ('Outdoor', 'Volunteer Outdoor')
    )
    STATUS = (
        ('Accepted', 'Accepted'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    )
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    date_of_birth = models.DateField(auto_now_add=False, null=True)
    education_background = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    occupation = models.CharField(max_length=200, null=True)
    way_of_contribution = models.CharField(max_length=200, null=True, choices=CONTRIBUTE)
    hours_per_day = models.CharField(max_length=20, null=True)
    application_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=50, null=True, default='Pending')
