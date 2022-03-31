import uuid as uuid
from django.db import models
from account.models import AccountUser, UserProfile
from model_utils.managers import InheritanceManager
from ckeditor.fields import RichTextField
from datetime import datetime


class Case(models.Model):
    STATUS = (
        ('Green', 'Green'),
        ('Orange', 'Orange'),
        ('Red', 'Red'),
        ('Closed', 'Closed'),
    )
    thumbnail = models.ImageField(null=True, blank=True, default='static/assets/img/default-thumbnail.jpg')
    title = models.CharField(max_length=100, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, null=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    requested_amount = models.FloatField(null=True, blank=True, default=0.0)
    total_collected = models.FloatField(null=True, blank=True, default=0.0)
    total_online = models.FloatField(null=True, blank=True, default=0.0)
    priority = models.IntegerField(null=True, blank=True, default=0)
    date_of_initiation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    other_financial_assistance = models.CharField(max_length=100, null=True, blank=True)
    verified_by = models.ForeignKey(AccountUser, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, null=True, choices=STATUS, default='Orange')

    objects = InheritanceManager()

    def __str__(self):
        return self.title

    def get_proper_child(self):
        return getattr(self, f'{self.type.lower()}case')

    @property
    def proper_total(self):
        online = self.total_online or 0.0
        offline = self.total_collected or 0.0
        return online + offline

    @property
    def has_finished(self):
        total = self.proper_total
        if total >= float(self.requested_amount or 0.0):
            self.status = 'Closed'
            self.save()
            return True
        else:
            return False

    @property
    def custom_id(self):
        year = self.date_of_initiation.year
        types = {
            'General': 'Gen', 'Educational': 'EDU', 'Medical': 'MEDL', 'Medicine': 'MEDN',
            'Provisional': "PRO"
        }
        return f'{year}{types[str(self.type)]}{self.pk}'


class EducationalCase(Case):
    # fields for education (death cert for orphan)category
    is_orphan = models.BooleanField(null=True, blank=True)
    death_cert = models.FileField(null=True, blank=True)
    guardian = models.CharField(max_length=200, null=True, blank=True)
    name_of_school = models.CharField(max_length=100, null=True, blank=True)
    location_of_school = models.CharField(max_length=200, null=True, blank=True)
    grade = models.CharField(max_length=10, null=True, blank=True)
    fee_structure = models.FileField(null=True, blank=True)


class GeneralCase(Case):
    # fields for general category
    nature_of_aid = models.CharField(max_length=200, null=True, blank=True)
    estimated_cost_cert = models.FileField(null=True, blank=True)


class MedicalCase(Case):
    # fields for medical category (and for 3 fields of medicine)
    nature_of_disease = models.CharField(max_length=50, null=True, blank=True)
    admitted_in_hospital = models.BooleanField(null=True, blank=True)
    name_of_hospital = models.CharField(max_length=50, null=True, blank=True)
    estimation_letter = models.FileField(null=True, blank=True)


class MedicineCase(Case):
    # medicine
    nature_of_disease = models.CharField(max_length=50, null=True, blank=True)
    name_of_hospital = models.CharField(max_length=50, null=True, blank=True)
    estimation_letter = models.FileField(null=True, blank=True)
    name_of_medicine = models.CharField(max_length=100, null=True, blank=True)


class ProvisionalCase(Case):
    # fields for provisional case
    MARITAL_STATUS = (
        ('Unmarried', 'Unmarried'),
        ('Married', 'Married'),
        ('Single', 'Single'),
        ('Widow', 'Widow'),
    )
    death_cert = models.FileField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, null=True, blank=True, choices=MARITAL_STATUS)


class ProjectDonation(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    donor = models.ForeignKey(AccountUser, null=True, on_delete=models.CASCADE, blank=True)
    full_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=55, null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=55, null=True)
    state = models.CharField(max_length=75, null=True)
    country = models.CharField(max_length=55, null=True)
    pan = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(auto_now_add=False, null=True)
    gender = models.CharField(max_length=20, null=True, choices=GENDER)
    transaction_id = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    case = models.ForeignKey(Case, null=True, on_delete=models.SET_NULL, blank=True)


class FamilyMembers(models.Model):
    name = models.CharField(max_length=30, null=True)
    age = models.CharField(max_length=4, null=True)
    monthly_income = models.IntegerField(null=True)
    relation = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    verified = models.BooleanField(default=False, null=True)


class ClosedDocs(models.Model):
    case = models.ForeignKey(Case, null=True, blank=True, on_delete=models.CASCADE)
    doc = models.FileField(null=True, blank=True)


class ExtraDocs(models.Model):
    case = models.ForeignKey(Case, null=True, blank=True, on_delete=models.CASCADE)
    doc = models.FileField(null=True, blank=True)


class ExtraImages(models.Model):
    case = models.ForeignKey(Case, null=True, blank=True, on_delete=models.CASCADE)
    img = models.ImageField(null=True, blank=True)