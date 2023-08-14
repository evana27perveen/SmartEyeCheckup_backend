import re
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        # Create a profile for the user
        # ProfileModel.objects.create(user=user)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email,
                                password=password,
                                **extra_fields
                                )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log in this site')
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    # Add related_name to prevent reverse accessor clashes
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     verbose_name='groups',
    #     blank=True,
    #     related_name='customuser_set',
    #     related_query_name='user'
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     verbose_name='user permissions',
    #     blank=True,
    #     related_name='customuser_set',
    #     related_query_name='user'
    # )


class DoctorProfileModel(models.Model):
    GENDER_OPTION = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="doctor_profile")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_OPTION, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)
    specialization = models.CharField(max_length=500, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'Doctor Profile - {self.full_name}'


class PatientProfileModel(models.Model):
    GENDER_OPTION = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_OPTION, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Patient Profile - {self.full_name}'
