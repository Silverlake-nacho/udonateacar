from __future__ import annotations

from django.db import models


class Barometer(models.Model):
    name = models.CharField("Name", max_length=64)
    value = models.PositiveIntegerField(default=0)
