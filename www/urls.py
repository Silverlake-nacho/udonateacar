from __future__ import annotations

from django.conf import settings
from django.urls import include, path

from . import debug_views, views

app_name = "www"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/v0/", include("www.api_urls")),
    path("capture/<str:step>", views.capture, name="capture"),
    path("charities", views.charities, name="charities"),
    path("faqs", views.faqs, name="faqs"),
    path("news", views.news, name="news"),
    path("news/<int:pk>", views.news_single, name="news_single"),
    path("testimonials", views.testimonials, name="testimonials"),
    path("vreawards", views.vre_awards, name="vre_awards"),
    path("awards", views.vre_awards, name="awards"),
    path("about", views.about, name="about"),
    path("how-it-works", views.how_it_works, name="how_it_works"),
    path("contact", views.contact, name="contact"),
    path("privacy", views.privacy, name="privacy"),
    path("awards-page/<str:slug>", views.custom_awards_page, name="custom_awards_page"),
]

debug_patterns = [
    path(
        "debug/",
        include(
            [
                path("crash", debug_views.crash),
                path("timeout", debug_views.timeout),
                path("status/<int:status_code>", debug_views.status_code),
                path("session", debug_views.session),
            ]
        ),
    ),
]

if settings.DEBUG:
    urlpatterns.extend(debug_patterns)
