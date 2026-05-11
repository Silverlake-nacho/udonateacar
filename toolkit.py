from __future__ import annotations

import math
from typing import Any, Dict

from django.db.models import QuerySet
from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR", "")
    return ip


def generate_pagination_context(
    objects: QuerySet[Any],
    request: HttpRequest,
    page_size: int = 6,
) -> Dict[str, Any]:
    page = int(request.GET.get("page", "1"))
    count = objects.count()
    page_start = (page - 1) * page_size
    on_page = objects[page_start : page_start + page_size]
    total_pages = math.ceil(count / page_size)

    page_list_start = max([1, page - 2])
    page_list_end = min([total_pages, page + 2])
    page_list = range(page_list_start, page_list_end + 1)

    previous_page = next_page = None

    if page > 1:
        previous_page = page - 1
    elif page < total_pages:
        next_page = page + 1

    url_no_page = request.build_absolute_uri("?")

    return {
        "objects": on_page,
        "count": count,
        "page": page,
        "total_pages": total_pages,
        "page_list": [{"id": x, "link": f"{url_no_page}?page={x}"} for x in page_list],
        "previous_page": f"{url_no_page}?page={previous_page}"
        if previous_page
        else None,
        "next_page": f"{url_no_page}?page={next_page}" if next_page else None,
    }


def suffix(day: int) -> str:
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]
