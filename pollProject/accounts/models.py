from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    REGIONS = [
        ('', 'Select Region'),
        ('AS', 'Asia'),
        ('EU', 'Europe'),
        ('NA', 'North America'),
        ('SA', 'South America'),
        ('AU', 'Oceania'),
        ('AF', 'Africa'),
        ('PH', 'Local (PH)'),
    ]

    GENDERS = [
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    region = models.CharField(max_length=2, choices=REGIONS, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username