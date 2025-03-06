from django.db import models
from django.conf import settings
from jalali_date import date2jalali


class InsulinType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    is_available = models.BooleanField(default=True)
    onset = models.CharField(
        max_length=20, help_text="Duration range (e.g., '15–30 min')")
    peak_time = models.CharField(
        max_length=20, help_text="Duration range (e.g., '15–30 min')")
    duration = models.CharField(
        max_length=20, help_text="Duration range (e.g., '15–30 min')")
    method = models.CharField(
        max_length=50,
        choices=[
            ('subcutaneous', 'Subcutaneous Injection'),
            ('intravenous', 'Intravenous Injection'),
            ('inhaled', 'Inhaled Insulin'),
            ('oral', 'Oral Insulin'),
            ('others', 'Others')
        ],
        default='subcutaneous',
        help_text="Method of insulin administration"
    )
    info = models.TextField(blank=True)

    def __str__(self):
        return self.name


class InjectionSites(models.Model):
    name = models.CharField(max_length=20)
    sites = models.CharField(max_length=20)


class Medication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    is_insulin = models.BooleanField(default=False)
    insulin_type = models.CharField(max_length=30)
    is_pill = models.BooleanField(default=False)


class Bloodcheck(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    bloodsugar = models.PositiveIntegerField(
        null=True, blank=True)
    time = models.TimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    event = models.CharField(max_length=30, null=True, blank=True)


class InsulinInjection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    insulin_type = models.CharField(max_length=30)
    insulin_dose = models.DecimalField(
        max_digits=4,
        decimal_places=2,
    )
    time = models.TimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    injection_site = models.CharField(max_length=20)


class Food(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    food = models.TextField(blank=True, null=True)
    carbs = models.PositiveIntegerField(null=True)
    time = models.TimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
