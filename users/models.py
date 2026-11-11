import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        db_table = "base_users"

    def __str__(self):
        return self.username