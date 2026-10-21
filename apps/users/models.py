from django.contrib.auth.models import AbstractUser
from django.db import models
from djangoc.core.validators import MaxLengthValidator

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/', default='users/default.png')
    level = models.IntegerField(validators=[MinValueValidator(1)], default=1)