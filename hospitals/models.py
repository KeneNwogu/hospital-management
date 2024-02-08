import uuid
import re

from django.db import models
from django.core.exceptions import ValidationError


def phone_number_validator(value):
    if not re.match(r'^(\+?234|0)([789]\d{9})$', value):
        raise ValidationError('Invalid phone number')


class Hospital(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False, validators=[phone_number_validator])
    website = models.URLField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name