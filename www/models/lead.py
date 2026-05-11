from __future__ import annotations

from io import BytesIO

from django.conf import settings
from django.core import files
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.utils import timezone

import requests

import apis.postcodes
import apis.vehicle_data


class Lead(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True)

    first_name = models.CharField("First Name", max_length=64, null=True, blank=True)
    last_name = models.CharField("Last Name", max_length=64, null=True, blank=True)
    email = models.EmailField("Email", max_length=64, null=True, blank=True)
    phone = models.CharField("Phone", max_length=64, null=True, blank=True)

    street = models.CharField("Street", max_length=64, null=True, blank=True)
    house_flat_number = models.CharField(
        "House / Flat Number", max_length=64, null=True, blank=True
    )
    city = models.CharField("Town / City", max_length=64)
    postcode = models.CharField("Post Code", max_length=10)
    nice_location = models.CharField("Nice Location", max_length=512)

    registration = models.CharField("Reg Number", max_length=10)
    car = models.CharField("Car", max_length=256)
    engine = models.CharField("Engine", max_length=256)
    color = models.CharField("Color", max_length=64)
    has_v5 = models.BooleanField("Has V5", default=True)
    wheels_on = models.BooleanField("Wheels On", default=True)
    drop_off = models.BooleanField("Drop Off", default=False)

    ip_address = models.GenericIPAddressField("IP Address", null=True, blank=True)

    def send(self) -> None:
        now = timezone.now()

        content = (
            f"Name: {self.first_name} {self.last_name}\n"
            f"Email: {self.email}\n"
            f"Phone: {self.phone}\n"
            f"Registration: {self.registration}\n"
            f"Postcode: {self.postcode}\n"
            f"Has V5: {self.wheels_on}\n"
            f"Wheels On: {self.wheels_on}\n"
            f"Can Drop Off: {self.drop_off}"
        )

        msg = EmailMultiAlternatives(
            f"From UDAC {now.isoformat()}",
            content,
            "server@udonateacar.com",
            [settings.LEAD_EMAIL],
        )

        for image in self.images.filter(primary=False):
            msg.attach(str(image.image), image.image)

        msg.send()

        self.sent_at = now
        self.save(update_fields=["sent_at"])

    @classmethod
    def from_basic(cls, ip: str, registration: str, postcode: str) -> Lead:
        car_lookup = apis.vehicle_data.lookup(registration)
        car_image = apis.vehicle_data.image(registration)
        location_lookup = apis.postcodes.lookup(postcode)

        engine_description = ""

        if fuel := car_lookup.get("FuelType"):
            engine_description += fuel + " "

        if transmission := car_lookup.get("Transmission"):
            engine_description += transmission + " "

        if capacity := car_lookup.get("EngineCapacity"):
            engine_description += capacity + "cc"

        lead = Lead.objects.create(
            city=location_lookup["admin_district"],
            postcode=postcode,
            nice_location=f"{location_lookup['admin_ward']}, "
            f"{location_lookup['admin_district']}, "
            f"{location_lookup['admin_county']}",
            registration=registration,
            car=f"{car_lookup['Make']} {car_lookup['Model']} {car_lookup['YearOfManufacture']}",
            engine=engine_description,
            color=car_lookup["Colour"],
            ip_address=ip,
        )

        image_request = requests.get(car_image)
        image_bytes = image_request.content
        logo_io = BytesIO()
        logo_io.write(image_bytes)

        image = VehicleImage.objects.create(
            lead=lead,
            primary=True,
        )

        image.image.save(f"{registration}.png", files.File(logo_io))
        image.save()

        return lead

    @property
    def stock_image_url(self):
        primary = self.images.get(primary=True)
        return primary.image.url


class VehicleImage(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vehicle_images/")
    primary = models.BooleanField("Primary", default=False)
