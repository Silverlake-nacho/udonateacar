from __future__ import annotations

from typing import Any, Dict

import requests

ENTRY_POINT = "https://uk1.ukvehicledata.co.uk/api/datapackage"
PARAMS: Dict[str, Any] = {
    "v": 2,
    "auth_apikey": "43f3e459-4f48-4eca-a42a-1078ba8fa16d",
}


def lookup(vrm: str) -> Dict[str, Any]:
    uri = f"{ENTRY_POINT}/VehicleData"
    params = dict(key_VRM=vrm, **PARAMS)
    response = requests.get(uri, params=params)

    try:
        data = response.json()["Response"]["DataItems"]["VehicleRegistration"]

        assert data.get("Make") and data.get("Model") and data.get("YearOfManufacture")
    except (KeyError, AssertionError):
        raise VehicleDataException("Unexpected API response")

    return data


def image(vrm: str) -> str:
    uri = f"{ENTRY_POINT}/VehicleImageData"
    params = dict(key_VRM=vrm, **PARAMS)
    response = requests.get(uri, params=params)
    data = response.json()

    try:
        images_list = data["Response"]["DataItems"]["VehicleImages"]["ImageDetailsList"]
        image_url = images_list[0]["ImageUrl"]
    except (IndexError, KeyError):
        raise VehicleDataException("Unexpected API response")

    return image_url


class VehicleDataException(Exception):
    pass
