"""Domo authentication and shared HTTP client.

All requests use a single developer token injected via the
X-DOMO-DEVELOPER-TOKEN header. No OAuth flow or token refresh.

Environment variables (required):
    DOMO_INSTANCE_URL    — e.g. https://yourcompany.domo.com
    DOMO_DEVELOPER_TOKEN — developer token from the Domo admin panel

Both variables are read lazily at call time so that load_dotenv() in
server.py is guaranteed to have run before the values are consumed,
regardless of import order.
"""
from __future__ import annotations

import os
from typing import Any

import httpx


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class DomoConfigError(RuntimeError):
    """DOMO_INSTANCE_URL or DOMO_DEVELOPER_TOKEN is not set."""


class DomoHTTPError(RuntimeError):
    """A Domo API request returned a non-2xx status code."""

    def __init__(self, response: httpx.Response) -> None:
        self.status_code = response.status_code
        self.response = response
        try:
            detail = response.json()
        except Exception:
            detail = response.text or "(empty body)"
        super().__init__(f"Domo API {response.status_code} — {response.url}: {detail}")


# ---------------------------------------------------------------------------
# Config helpers (lazy — read at call time, not import time)
# ---------------------------------------------------------------------------

def _instance_url() -> str:
    url = os.environ.get("DOMO_INSTANCE_URL", "").rstrip("/")
    if not url:
        raise DomoConfigError(
            "DOMO_INSTANCE_URL is not set. "
            "Add it to your .env file or environment."
        )
    return url


def _token() -> str:
    token = os.environ.get("DOMO_DEVELOPER_TOKEN", "")
    if not token:
        raise DomoConfigError(
            "DOMO_DEVELOPER_TOKEN is not set. "
            "Add it to your .env file or environment."
        )
    return token


def base_url() -> str:
    return f"{_instance_url()}/api"


def get_headers() -> dict[str, str]:
    return {
        "X-DOMO-DEVELOPER-TOKEN": _token(),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _client() -> httpx.Client:
    return httpx.Client(
        base_url=base_url(),
        headers=get_headers(),
        timeout=30.0,
    )


def _clean_params(params: dict[str, Any]) -> dict[str, Any]:
    """Strip None values so optional query params are omitted from the URL."""
    return {k: v for k, v in params.items() if v is not None}


def _parse(response: httpx.Response) -> Any:
    """Raise DomoHTTPError on non-2xx; return parsed body on success.

    Returns:
        Parsed JSON (dict or list), plain text string, or None for empty
        bodies (e.g. 204 No Content).
    """
    if not response.is_success:
        raise DomoHTTPError(response)
    if not response.content:
        return None
    content_type = response.headers.get("content-type", "")
    if "json" in content_type:
        return response.json()
    return response.text


# ---------------------------------------------------------------------------
# Public HTTP verbs — used by every tool module
# ---------------------------------------------------------------------------

def get(path: str, **params: Any) -> Any:
    with _client() as c:
        return _parse(c.get(path, params=_clean_params(params)))


def get_root(path: str, **params: Any) -> Any:
    """GET against a path rooted at the instance URL (no /api prefix)."""
    with httpx.Client(base_url=_instance_url(), headers=get_headers(), timeout=30.0) as c:
        return _parse(c.get(path, params=_clean_params(params)))


def post(path: str, body: Any = None, **params: Any) -> Any:
    with _client() as c:
        return _parse(c.post(path, json=body, params=_clean_params(params)))


def put(path: str, body: Any = None, **params: Any) -> Any:
    with _client() as c:
        return _parse(c.put(path, json=body, params=_clean_params(params)))


def patch(path: str, body: Any = None, **params: Any) -> Any:
    with _client() as c:
        return _parse(c.patch(path, json=body, params=_clean_params(params)))


def delete(path: str, body: Any = None, **params: Any) -> Any:
    with _client() as c:
        # httpx.Client has no .delete(..., json=...) shorthand
        return _parse(c.request("DELETE", path, json=body, params=_clean_params(params)))


def delete_root(path: str, **params: Any) -> Any:
    """DELETE against a path rooted at the instance URL (no /api prefix)."""
    with httpx.Client(base_url=_instance_url(), headers=get_headers(), timeout=30.0) as c:
        return _parse(c.request("DELETE", path, params=_clean_params(params)))


def post_no_body(path: str, **params: Any) -> Any:
    """POST with only query params and no request body (no Content-Type header)."""
    headers = {k: v for k, v in get_headers().items() if k != "Content-Type"}
    with httpx.Client(base_url=base_url(), headers=headers, timeout=30.0) as c:
        return _parse(c.post(path, params=_clean_params(params)))


def put_text(path: str, text: str, content_type: str = "text/csv", **params: Any) -> Any:
    """PUT a raw text body (e.g. CSV data for multi-part dataset uploads).

    Uses a 120-second timeout — appropriate for large data payloads.
    """
    headers = get_headers()
    headers["Content-Type"] = content_type
    with httpx.Client(base_url=base_url(), headers=headers, timeout=120.0) as c:
        return _parse(c.put(path, content=text.encode(), params=_clean_params(params)))


def post_multipart(
    path: str,
    file_name: str,
    file_bytes: bytes,
    mime_type: str = "application/octet-stream",
    extra_fields: dict[str, str] | None = None,
    **params: Any,
) -> Any:
    """POST a multipart/form-data file upload.

    Content-Type (with boundary) is set automatically by httpx when using the
    files= parameter — do NOT set it manually or the boundary will be missing.
    Uses a 120-second timeout for large files.
    """
    headers = {
        "X-DOMO-DEVELOPER-TOKEN": _token(),
        "Accept": "application/json",
    }
    files = {"file": (file_name, file_bytes, mime_type)}
    with httpx.Client(base_url=base_url(), headers=headers, timeout=120.0) as c:
        return _parse(
            c.post(
                path,
                files=files,
                data=extra_fields or {},
                params=_clean_params(params),
            )
        )
