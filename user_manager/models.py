from django.db import models
import uuid

from django.contrib.auth.models import User
from timestampedmodel import TimestampedModel

class UserMetadata(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
