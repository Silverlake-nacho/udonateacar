from __future__ import annotations

from django.urls import path

from www import api_views

urlpatterns = [
    path("create-lead", api_views.create_lead, name="create_lead"),
    path("save-vehicle-image", api_views.save_vehicle_image, name="save_vehicle_image"),
    path(
        "delete-vehicle-image",
        api_views.delete_vehicle_image,
        name="delete_vehicle_image",
    ),
    path("save-answers", api_views.save_answers, name="save_answers"),
]
