from __future__ import annotations

from typing import Any, Dict

import requests

ENTRY_POINT = "https://api.postcodes.io/postcodes"


def lookup(postcode: str) -> Dict[str, Any]:
    uri = f"{ENTRY_POINT}/{postcode}"
    response = requests.get(uri)
    result = response.json()["result"]

    try:
        assert (
            "admin_county" in result
            and "admin_district" in result
            and "admin_ward" in result
        )
    except AssertionError:
        raise PostcodesException("Unrecognized API response")

    return result


class PostcodesException(Exception):
    pass
