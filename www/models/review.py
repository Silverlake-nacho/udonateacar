from __future__ import annotations

import urllib.parse as urlparse
from typing import Optional

from django.db import models
from django.db.models import QuerySet
from django.db.models.functions import Length

import toolkit


class Review(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField("Name", max_length=128)
    content = models.TextField()
    active = models.BooleanField(default=True)

    youtube_url = models.CharField(
        "YouTube Link", max_length=512, null=True, blank=True
    )
    image = models.ImageField("Image", upload_to="reviews", null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls) -> QuerySet[Review]:
        return Review.objects.filter(active=True, image=None).exclude(youtube_url__isnull=False).order_by(
            Length("content").desc()
        )

    @classmethod
    def get_active_video(cls) -> QuerySet[Review]:
        videos = Review.objects.filter(active=True, youtube_url__isnull=False)
        valid = [x.id for x in videos if x.embed_link]
        images = Review.objects.filter(active=True, image__isnull=False)
        valid_images = [x.id for x in images]

        return Review.objects.filter(id__in=valid + valid_images).order_by(
            "-created_at"
        )

    @property
    def embed_link(self) -> Optional[str]:
        if not self.youtube_url:
            return None

        parsed_url = urlparse.urlparse(self.youtube_url)

        if "youtu.be" in self.youtube_url:
            youtube_id = parsed_url.path[1:]
        else:
            try:
                youtube_id = urlparse.parse_qs(parsed_url.query)["v"][0]
            except KeyError:
                return None

        return f"https://www.youtube.com/embed/{youtube_id}?controls=0&showinfo=0&rel=0"

    @property
    def nice_date(self) -> str:
        day = self.created_at.day
        suffix = toolkit.suffix(day)
        rest = self.created_at.strftime("%B %Y")

        return f"{day}{suffix} {rest}"
