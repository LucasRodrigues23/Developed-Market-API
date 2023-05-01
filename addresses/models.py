from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=30)
    street = models.CharField(max_length=50)
    number = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    complement = models.CharField(max_length=100, null=True, blank=True, default=None)
