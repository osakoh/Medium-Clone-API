import uuid

from django.db import models


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # model instance is created for the first time
    updated_at = models.DateTimeField(
        auto_now=True
    )  # anytime .save() method is called on the model instance

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]  # reverse chronology
