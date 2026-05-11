from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import include, path

from .sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")),
    path("admin/", admin.site.urls),
    path("summernote/", include("django_summernote.urls")),
    path("sitemap.xml", sitemap_views.sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", include("www.urls")),
]

urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_URL))
urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
