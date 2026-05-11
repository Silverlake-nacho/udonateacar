from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"
    protocol = "https"

    def items(self):
        return [
            "www:index",
            "www:contact",
            "www:privacy",
        ]

    def location(self, item):
        return reverse(item)
