from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class AccountUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError('All Users Must Have An Email address')

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=self.normalize_email(email),
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AccountUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = AccountUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_group(self):
        group = 'user'
        if self.groups.exists():
            group = self.groups.first().name
        return group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    HOUSE = (
        ('Owned', 'Owned'),
        ('Leased', 'Leased'),
        ('Rented', 'Rented')
    )
    user = models.ForeignKey(AccountUser, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=55, null=True)
    state = models.CharField(max_length=75, null=True)
    country = models.CharField(max_length=55, null=True)
    pan = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateField(auto_now_add=False, null=True)
    house_ownership = models.CharField(max_length=30, null=True, choices=HOUSE, blank=True)
    rent_amount = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, choices=GENDER)

    def __str__(self):
        return self.user.first_name