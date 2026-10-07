from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        FEMALE = 'F', 'Female'
        MALE = 'M', 'Male'
        OTHER = 'O', 'Other'

    avatar = models.ImageField(upload_to='user/avatar/', blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=True)
