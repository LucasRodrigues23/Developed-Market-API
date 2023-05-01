from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(max_length=127, unique=True)

    bio = models.TextField(null=True, blank=True, default=None)
    birthdate = models.DateField(null=True, blank=True)

    is_seller = models.BooleanField(null=True, default=False)
    is_client = models.BooleanField(null=True, default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
