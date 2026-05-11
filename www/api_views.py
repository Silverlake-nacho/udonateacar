from __future__ import annotations

import json
from typing import cast

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

from apis.postcodes import PostcodesException
from apis.vehicle_data import VehicleDataException
from toolkit import get_client_ip
from www.models import Lead
from www.models.lead import VehicleImage


def create_lead(request: HttpRequest) -> JsonResponse:
    body = json.loads(request.body)

    try:
        vrm = cast(str, body["vrm"])
        postcode = cast(str, body["postcode"])
    except KeyError:
        return JsonResponse({"message": "missing either vrm or postcode"}, status=400)

    try:
        lead = Lead.from_basic(get_client_ip(request), vrm, postcode)
    except (PostcodesException, VehicleDataException) as error:
        return JsonResponse(
            {"message": f"vehicle lookup error - '{error}'"}, status=400
        )

    request.session["lead_id"] = lead.id

    return JsonResponse(
        {
            "message": "success",
        }
    )


def save_vehicle_image(request: HttpRequest) -> HttpResponse:
    try:
        lead = Lead.objects.get(id=request.session["lead_id"])
        image = request.FILES["file"]
    except (KeyError, Lead.DoesNotExist):
        return HttpResponseBadRequest()

    VehicleImage.objects.create(
        lead=lead,
        image=image,
    )

    return JsonResponse({"message": "success"})


def delete_vehicle_image(request: HttpRequest) -> HttpResponse:
    try:
        lead = Lead.objects.get(id=request.session["lead_id"])
    except (KeyError, Lead.DoesNotExist):
        return HttpResponseBadRequest()

    try:
        body = json.loads(request.body)
        image_name = body["image"]
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest()

    VehicleImage.objects.filter(
        lead=lead,
        image__contains=image_name,
    ).delete()

    return JsonResponse({"message": "success"})


def save_answers(request: HttpRequest) -> HttpResponse:
    try:
        lead = Lead.objects.get(id=request.session["lead_id"])
    except (KeyError, Lead.DoesNotExist):
        return HttpResponseBadRequest()

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest()

    try:
        page = body["url"]
        answers = body["answers"]
    except KeyError:
        return HttpResponseBadRequest()

    send_lead = False

    if page == "/capture/contact":
        name = answers["name"]
        first_name = name.split(" ")[0]
        last_name = name.split(" ")[-1]

        lead.first_name = first_name
        lead.last_name = last_name
        lead.phone = answers["phone"]
        lead.email = answers["email"]
    elif page == "/capture/collection":
        send_lead = True

        lead.street = answers["street"]
        lead.house_flat_number = answers["house_flat_number"]
        lead.city = answers["city"]
        lead.postcode = answers["postcode"]
        lead.has_v5 = answers["has_v5"] == "yes"
        lead.wheels_on = answers["wheels_on"] == "yes"

        lead.nice_location = (
            f"{lead.house_flat_number}, {lead.street}, {lead.city}, {lead.postcode}"
        )

    lead.save()

    if send_lead:
        lead.send()

    return JsonResponse({"message": "success"})
