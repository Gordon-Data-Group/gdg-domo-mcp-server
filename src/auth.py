"""Domo authentication, instance selection, and shared HTTP client.

All requests use a developer token injected via the X-DOMO-DEVELOPER-TOKEN
header. No OAuth flow or token refresh.

Single instance (environment variables):
    DOMO_INSTANCE_URL    — e.g. https://yourcompany.domo.com
    DOMO_DEVELOPER_TOKEN — developer token from the Domo admin panel
    DOMO_READ_ONLY       — optional, default "1"

Multiple instances from one server process:
    DOMO_INSTANCES                 — comma-separated aliases, e.g. "gdg,rove"
    DOMO_<ALIAS>_INSTANCE_URL      — per-alias instance URL
    DOMO_<ALIAS>_DEVELOPER_TOKEN   — per-alias developer token
    DOMO_<ALIAS>_READ_ONLY         — optional per-alias override of DOMO_READ_ONLY
    DOMO_DEFAULT_INSTANCE          — optional; defaults to the first alias

<ALIAS> is the alias upper-cased with non-alphanumerics replaced by "_".
Every tool gains an `instance` argument when more than one alias is
configured; src/toolsets.py activates the chosen instance for the duration
of the call via `use_instance()`.

All variables are read lazily at call time so that load_dotenv() in
server.py is guaranteed to have run before the values are consumed,
regardless of import order.
"""
from __future__ import annotations

import os
import re
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Iterator

import httpx


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class DomoConfigError(RuntimeError):
    """Instance URL or developer token is missing or invalid."""


class DomoHTTPError(RuntimeError):
    """A Domo API request returned a non-2xx status code."""

    def __init__(self, response: httpx.Response) -> None:
        self.status_code = response.status_code
        self.response = response
        try:
            detail = response.json()
        except Exception:
            detail = response.text or "(empty body)"
        # Strip query string so tokens or sensitive params never appear in traces.
        url = response.url.copy_with(query=None)
        super().__init__(f"Domo API {response.status_code} — {url}: {detail}")


# ---------------------------------------------------------------------------
# Instance configuration (lazy — read at call time, not import time)
# ---------------------------------------------------------------------------

SINGLE_INSTANCE_ALIAS = "default"
FALSY_VALUES = ("0", "false", "no", "off")


@dataclass(frozen=True)
class Instance:
    alias: str
    env_prefix: str  # "DOMO_" for the single-instance form, "DOMO_<ALIAS>_" otherwise

    def _env(self, suffix: str) -> str:
        return os.environ.get(f"{self.env_prefix}{suffix}", "").strip()

    @property
    def url(self) -> str:
        url = self._env("INSTANCE_URL").rstrip("/")
        if not url:
            raise DomoConfigError(
                f"{self.env_prefix}INSTANCE_URL is not set. "
                "Add it to your .env file or environment."
            )
        host = httpx.URL(url).host.lower()
        if not (host.endswith(".domo.com") or host == "domo.com"):
            raise DomoConfigError(
                f"{self.env_prefix}INSTANCE_URL host '{host}' is not a domo.com domain. "
                "Expected format: https://yourcompany.domo.com"
            )
        return url

    @property
    def token(self) -> str:
        token = self._env("DEVELOPER_TOKEN")
        if not token:
            raise DomoConfigError(
                f"{self.env_prefix}DEVELOPER_TOKEN is not set. "
                "Add it to your .env file or environment."
            )
        return token

    @property
    def read_only(self) -> bool:
        """True unless this instance's (or the global) DOMO_READ_ONLY is falsy.

        Defaults to read-only so a freshly configured server can never mutate
        Domo data until an operator deliberately opts in via the environment.
        """
        raw = self._env("READ_ONLY") or os.environ.get("DOMO_READ_ONLY", "1")
        return raw.strip().lower() not in FALSY_VALUES


def _env_prefix(alias: str) -> str:
    return f"DOMO_{re.sub(r'[^A-Za-z0-9]', '_', alias).upper()}_"


def instances() -> dict[str, Instance]:
    """Configured instances keyed by alias, in DOMO_INSTANCES order."""
    raw = os.environ.get("DOMO_INSTANCES", "").strip()
    if not raw:
        return {SINGLE_INSTANCE_ALIAS: Instance(SINGLE_INSTANCE_ALIAS, "DOMO_")}
    aliases = [a.strip() for a in raw.split(",") if a.strip()]
    return {a: Instance(a, _env_prefix(a)) for a in aliases}


def default_alias() -> str:
    configured = instances()
    alias = os.environ.get("DOMO_DEFAULT_INSTANCE", "").strip()
    if alias:
        if alias not in configured:
            raise DomoConfigError(
                f"DOMO_DEFAULT_INSTANCE={alias!r} is not listed in DOMO_INSTANCES "
                f"({', '.join(configured)})."
            )
        return alias
    return next(iter(configured))


_active_alias: ContextVar[str | None] = ContextVar("domo_active_instance", default=None)


@contextmanager
def use_instance(alias: str | None) -> Iterator[Instance]:
    """Route every HTTP call inside the block to `alias` (None = default)."""
    configured = instances()
    alias = alias or default_alias()
    if alias not in configured:
        raise DomoConfigError(
            f"Unknown Domo instance {alias!r}. Configured: {', '.join(configured)}."
        )
    token = _active_alias.set(alias)
    try:
        yield configured[alias]
    finally:
        _active_alias.reset(token)


def current_instance() -> Instance:
    configured = instances()
    alias = _active_alias.get() or default_alias()
    if alias not in configured:
        raise DomoConfigError(
            f"Unknown Domo instance {alias!r}. Configured: {', '.join(configured)}."
        )
    return configured[alias]


def _instance_url() -> str:
    return current_instance().url


def _token() -> str:
    return current_instance().token


def base_url() -> str:
    return f"{_instance_url()}/api"


def read_only_mode() -> bool:
    """True when the active instance (default instance outside a call) is read-only.

    This is the single source of truth for read-only status at the HTTP layer
    — every mutating verb in this module consults it, so a tool mis-tagged as
    read-only still can't reach a mutating endpoint.
    """
    return current_instance().read_only


def all_instances_read_only() -> bool:
    """True when no configured instance allows writes.

    src/toolsets.py uses this to decide whether write tools are registered at
    all; the per-call check in _assert_write_allowed still applies on top.
    """
    return all(inst.read_only for inst in instances().values())


def _assert_write_allowed(path: str) -> None:
    inst = current_instance()
    if inst.read_only:
        if inst.alias == SINGLE_INSTANCE_ALIAS:
            hint = "Set DOMO_READ_ONLY=0 in your environment"
        else:
            hint = f"Set {inst.env_prefix}READ_ONLY=0 (or DOMO_READ_ONLY=0) in your environment"
        raise DomoConfigError(
            f"Blocked write request to '{path}' on instance '{inst.alias}': read-only "
            f"mode is enabled (default). {hint} to allow tools that create, update, "
            "or delete Domo data."
        )


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


def post_read(path: str, body: Any = None, **params: Any) -> Any:
    """POST to a non-mutating endpoint (search, query, bulk-get).

    Not subject to the read-only guard — use only for endpoints that never
    change Domo data, and only from tools tagged read_only=True.
    """
    with _client() as c:
        return _parse(c.post(path, json=body, params=_clean_params(params)))


def put_read(path: str, body: Any = None, **params: Any) -> Any:
    """PUT to a non-mutating endpoint (Domo serves some card reads over PUT).

    Same contract as post_read.
    """
    with _client() as c:
        return _parse(c.put(path, json=body, params=_clean_params(params)))


def post(path: str, body: Any = None, **params: Any) -> Any:
    _assert_write_allowed(path)
    return post_read(path, body, **params)


def put(path: str, body: Any = None, **params: Any) -> Any:
    _assert_write_allowed(path)
    return put_read(path, body, **params)


def patch(path: str, body: Any = None, **params: Any) -> Any:
    _assert_write_allowed(path)
    with _client() as c:
        return _parse(c.patch(path, json=body, params=_clean_params(params)))


def delete(path: str, body: Any = None, **params: Any) -> Any:
    _assert_write_allowed(path)
    with _client() as c:
        # httpx.Client has no .delete(..., json=...) shorthand
        return _parse(c.request("DELETE", path, json=body, params=_clean_params(params)))


def delete_root(path: str, **params: Any) -> Any:
    """DELETE against a path rooted at the instance URL (no /api prefix)."""
    _assert_write_allowed(path)
    with httpx.Client(base_url=_instance_url(), headers=get_headers(), timeout=30.0) as c:
        return _parse(c.request("DELETE", path, params=_clean_params(params)))


def post_no_body(path: str, **params: Any) -> Any:
    """POST with only query params and no request body (no Content-Type header)."""
    _assert_write_allowed(path)
    headers = {k: v for k, v in get_headers().items() if k != "Content-Type"}
    with httpx.Client(base_url=base_url(), headers=headers, timeout=30.0) as c:
        return _parse(c.post(path, params=_clean_params(params)))


def put_text(path: str, text: str, content_type: str = "text/csv", **params: Any) -> Any:
    """PUT a raw text body (e.g. CSV data for multi-part dataset uploads).

    Uses a 120-second timeout — appropriate for large data payloads.
    """
    _assert_write_allowed(path)
    headers = get_headers()
    headers["Content-Type"] = content_type
    with httpx.Client(base_url=base_url(), headers=headers, timeout=120.0) as c:
        return _parse(c.put(path, content=text.encode(), params=_clean_params(params)))


def get_bytes(path: str, **params: Any) -> bytes:
    """GET raw bytes (e.g. CSV/XLSX export data) without JSON parsing.

    Uses a 120-second timeout — export payloads can be large. Omits the
    default 'Accept: application/json' header so the server honors the
    format requested via query params (e.g. accept=text/csv).
    """
    headers = {k: v for k, v in get_headers().items() if k != "Accept"}
    with httpx.Client(base_url=base_url(), headers=headers, timeout=120.0) as c:
        response = c.get(path, params=_clean_params(params))
        if not response.is_success:
            raise DomoHTTPError(response)
        return response.content


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
    _assert_write_allowed(path)
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
