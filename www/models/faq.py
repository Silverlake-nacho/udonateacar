from __future__ import annotations

from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class Faq(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Creation Date", default=timezone.now, null=False
    )

    question = models.CharField("Question", max_length=512)
    answer = models.TextField()

    active = models.BooleanField(default=True)

    @classmethod
    def get_active(cls) -> QuerySet[Faq]:
        return Faq.objects.filter(active=True).order_by("-created_at")
