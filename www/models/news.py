from __future__ import annotations

from typing import Optional

from django.db import models
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

import toolkit


class News(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Creation Date", default=timezone.now, null=False
    )

    title = models.CharField("Title", max_length=512)
    category = models.CharField("Category", max_length=32, default="News")
    pre_content = models.TextField(null=True, blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="news-images/", null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @classmethod
    def get_active(cls) -> QuerySet[News]:
        return News.objects.filter(active=True).order_by("-created_at")

    @classmethod
    def get_featured(cls) -> Optional[News]:
        return News.objects.filter(featured=True).last()

    @property
    def link(self):
        return reverse("www:news_single", kwargs={"pk": self.id})

    @property
    def nice_date(self) -> str:
        day = self.created_at.day
        suffix = toolkit.suffix(day)
        rest = self.created_at.strftime("%B %Y")

        return f"{day}{suffix} {rest}"

    @property
    def blurb(self) -> str:
        return strip_tags(self.content)[:160] + "..."
