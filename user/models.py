from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    phone = models.TextField(blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
