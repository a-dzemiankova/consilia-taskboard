from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import make_aware


class User(AbstractUser):
    photo = models.ImageField(upload_to="users/%Y%m%d/", blank=True, null=True)
    date_birth = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_birth and self.date_birth.tzinfo is None:
            self.date_birth = make_aware(self.date_birth)
        super().save(*args, **kwargs)
