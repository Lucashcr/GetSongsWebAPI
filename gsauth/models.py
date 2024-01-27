from datetime import datetime, timedelta, timezone
import uuid

from django.contrib.auth.models import User
from django.db import models


def generate_token():
    return uuid.uuid4().hex


class PasswordRecoveryToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=generate_token, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_valid = models.BooleanField(default=True)

    @property
    def expired(self):
        return datetime.now(timezone.utc) > self.created_at + timedelta(minutes=30)
