from __future__ import annotations

import time
import typing

from django.http import FileResponse, JsonResponse

if typing.TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


def crash(request: HttpRequest) -> typing.NoReturn:
    raise Exception("All the king's horses, and all the king's men.")


def timeout(request: HttpRequest) -> typing.NoReturn:
    while True:
        time.sleep(1)


def status_code(request: HttpRequest, *, status_code: str) -> HttpResponse:
    return JsonResponse({}, status=status_code)


def session(request: HttpRequest) -> HttpResponse:
    request.session["session.debug"] = True
    return JsonResponse(dict(request.session.items()))


def static_file(request: HttpRequest, *, path: str) -> FileResponse:
    # Django docs say the file will be closed automatically, and not
    # to open it with a context manager
    return FileResponse(open(path, "rb"))
