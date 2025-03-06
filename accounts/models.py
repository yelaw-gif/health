from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="شماره تلفن باید 10 رقمی باشد"
)


class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=10, unique=True, blank=False, null=False, validators=[phone_validator])

    def __str__(self):
        return self.phone_number


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    USER_TYPES = (
        ('gp', 'general practitioner'),
        ('endocrinologist', 'Endocrinologist'),
    )
    user_type = models.CharField(
        max_length=30, choices=USER_TYPES, default='gp')
