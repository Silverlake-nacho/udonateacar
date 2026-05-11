from __future__ import annotations

from django.db import models
from django.utils import timezone

from www.models.news import News
from www.models.review import Review


class CustomPage(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Creation Date", default=timezone.now, null=False
    )
    slug = models.CharField("Slug", max_length=64)

    heading = models.CharField("Page Heading", max_length=256)
    subheading = models.TextField(null=True, blank=True)
    quote = models.TextField(null=True, blank=True)

    news_items = models.ManyToManyField(News)
    testimonial_items = models.ManyToManyField(Review)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.slug
