"""Render-compatible WSGI entrypoint.

Render's default Python start command may run ``gunicorn app:app``.  This
module exposes the Django WSGI application under that name while keeping the
canonical Django entrypoint in ``udac.wsgi``.
"""

from __future__ import annotations

from udac.wsgi import application as app
