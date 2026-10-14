"""Toolset registry and lazy tool registration for the Domo MCP server.

Every domain tool module (src/tools/*.py) registers its tools through the
`domo_tool` decorator defined here instead of calling `@mcp.tool()`
directly. That indirection is what makes two things possible:

1. DOMO_READ_ONLY (default "1" — read-only): tools tagged `read_only=False`
   are simply never attached to the server unless at least one configured
   instance has read-only turned off (DOMO_READ_ONLY=0 or a per-instance
   DOMO_<ALIAS>_READ_ONLY=0). This is belt-and-suspenders with the
   enforcement in src/auth.py, which blocks mutating HTTP verbs per call for
   whichever instance the call targets — so even a mis-tagged tool can't
   reach a write endpoint. Read-only tools whose endpoint happens to be a
   POST/PUT (search, query, bulk-get) must call auth.post_read/put_read.

2. DOMO_DYNAMIC_TOOLSETS (default "0" — off): when enabled, domain tools are
   *not* registered at startup. Only two meta-tools are exposed —
   `list_toolsets` and `enable_toolset` — and calling `enable_toolset`
   registers that group's tools on demand. This keeps the initial tool
   list (and its token cost) tiny for sessions that only need a few
   toolsets out of the ~35 available. DOMO_DEFAULT_TOOLSETS (comma-separated)
   can pre-enable specific toolsets at startup even in dynamic mode.

Registration also wraps each tool (see _build_tool_fn): string metadata in
Annotated[...] becomes a real schema description, an `instance` argument is
added when several Domo instances are configured, schemas are slimmed of
token-wasting boilerplate, and results are returned as compact JSON capped
at DOMO_MAX_RESPONSE_CHARS.

Every tool module must still be *imported* unconditionally (see
src/server.py) so its `domo_tool`-decorated functions run and populate the
registry below — dynamic mode defers *registration*, not *import*, which is
cheap (no I/O, just function definitions).
"""
from __future__ import annotations

import inspect
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Annotated, Any, Callable, Literal, get_args, get_origin, get_type_hints

from mcp.server.fastmcp import Context
from mcp.types import ToolAnnotations
from pydantic import Field

from src import auth
from src.app import mcp

TRUE_VALUES = {"1", "true", "yes", "on"}


def _env_bool(name: str, default: str) -> bool:
    return os.environ.get(name, default).strip().lower() in TRUE_VALUES


def dynamic_toolsets_enabled() -> bool:
    return _env_bool("DOMO_DYNAMIC_TOOLSETS", "0")


def _default_toolsets() -> set[str] | None:
    """Toolsets to pre-enable at startup under dynamic mode.

    Returns None when DOMO_DEFAULT_TOOLSETS is unset, meaning "nothing
    preloaded — the caller must enable_toolset() explicitly."
    """
    raw = os.environ.get("DOMO_DEFAULT_TOOLSETS", "").strip()
    if not raw:
        return None
    return {t.strip() for t in raw.split(",") if t.strip()}


@dataclass
class ToolRecord:
    name: str
    toolset: str
    read_only: bool
    func: Callable[..., Any]
    registered: bool = False


_registry: dict[str, ToolRecord] = {}
_by_toolset: dict[str, list[str]] = defaultdict(list)


def domo_tool(toolset: str, read_only: bool) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator replacing @mcp.tool() for every tool in src/tools/*.py.

    Args:
        toolset: Group name, matching the owning module (e.g. "datasets").
            Used by list_toolsets/enable_toolset and shown to the caller.
        read_only: Whether the underlying call is a pure read (GET, or a
            POST-with-body search/query/list endpoint that doesn't mutate
            Domo data). Write tools are skipped entirely while
            DOMO_READ_ONLY is enabled (the default).
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        name = func.__name__
        if name in _registry:
            raise ValueError(f"Duplicate tool name registered: {name!r}")
        record = ToolRecord(name=name, toolset=toolset, read_only=read_only, func=func)
        _registry[name] = record
        _by_toolset[toolset].append(name)

        if auth.all_instances_read_only() and not read_only:
            return func  # write tool suppressed under read-only mode

        if dynamic_toolsets_enabled():
            defaults = _default_toolsets()
            if defaults is None or toolset not in defaults:
                return func  # deferred until enable_toolset() is called

        _register(record)
        return func

    return decorator


def _register(record: ToolRecord) -> None:
    if record.registered:
        return
    mcp.add_tool(
        _build_tool_fn(record.func),
        name=record.name,
        annotations=ToolAnnotations(readOnlyHint=record.read_only),
        structured_output=False,
    )
    tool = mcp._tool_manager.get_tool(record.name)
    tool.parameters = _slim_schema(tool.parameters)
    record.registered = True


# ---------------------------------------------------------------------------
# Tool function wrapping — schema shaping, instance routing, output shaping
# ---------------------------------------------------------------------------

def _max_response_chars() -> int:
    """DOMO_MAX_RESPONSE_CHARS (default 50000; 0 disables truncation)."""
    try:
        return int(os.environ.get("DOMO_MAX_RESPONSE_CHARS", "50000"))
    except ValueError:
        return 50000


def _strip_nulls(value: Any) -> Any:
    """Drop null-valued dict keys, recursively. List positions are preserved
    (query rows are positional), so nulls inside lists are kept."""
    if isinstance(value, dict):
        return {k: _strip_nulls(v) for k, v in value.items() if v is not None}
    if isinstance(value, list):
        return [_strip_nulls(v) for v in value]
    return value


def format_result(result: Any) -> str:
    """Serialize a tool's return value for the model: compact JSON, nulls
    removed (unless DOMO_STRIP_NULLS=0), capped at DOMO_MAX_RESPONSE_CHARS.

    FastMCP's default is indent=2 JSON, which puts every scalar of a nested
    payload on its own indented line — expensive for query rows and lists.
    """
    if result is None:
        return "Success (empty response)."
    if isinstance(result, str):
        text = result
    else:
        if _env_bool("DOMO_STRIP_NULLS", "1"):
            result = _strip_nulls(result)
        text = json.dumps(result, separators=(",", ":"), ensure_ascii=False, default=str)
    limit = _max_response_chars()
    if limit > 0 and len(text) > limit:
        text = (
            f"{text[:limit]}\n…[truncated: showing {limit:,} of {len(text):,} characters. "
            "Narrow the request with limit/offset, filters, or a more selective query.]"
        )
    return text


def _describe(annotation: Any) -> Any:
    """Turn Annotated[T, "text"] into Annotated[T, Field(description="text")].

    Pydantic ignores bare strings in Annotated metadata, so without this every
    parameter description written in src/tools/*.py would be silently dropped
    from the JSON schema the model sees.
    """
    if get_origin(annotation) is not Annotated:
        return annotation
    base, *meta = get_args(annotation)
    meta = [Field(description=m) if isinstance(m, str) else m for m in meta]
    return Annotated[(base, *meta)]


def _build_tool_fn(func: Callable[..., Any]) -> Callable[..., str]:
    """Wrap a tool function with the signature/behaviour FastMCP should expose.

    - parameter descriptions become real Field descriptions (see _describe)
    - when several Domo instances are configured, an `instance` argument is
      appended and the call runs against that instance
    - the return value is serialized by format_result
    """
    hints = get_type_hints(func, include_extras=True)
    sig = inspect.signature(func)
    params = [p.replace(annotation=_describe(hints.get(p.name, p.annotation)))
              for p in sig.parameters.values()]

    aliases = list(auth.instances())
    if len(aliases) > 1:
        params.append(
            inspect.Parameter(
                "instance",
                inspect.Parameter.KEYWORD_ONLY,
                default=auth.default_alias(),
                annotation=Literal[tuple(aliases)],
            )
        )

    def wrapper(**kwargs: Any) -> str:
        with auth.use_instance(kwargs.pop("instance", None)):
            return format_result(func(**kwargs))

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    wrapper.__signature__ = sig.replace(parameters=params, return_annotation=str)  # type: ignore[attr-defined]
    return wrapper


def _slim_schema(schema: Any) -> Any:
    """Remove JSON-schema noise that costs tokens without informing the model:
    auto-generated `title`s, `default: null`, and `anyOf: [X, {type: null}]`
    wrappers around optional parameters (optional-ness is already conveyed by
    absence from `required`)."""
    if isinstance(schema, list):
        return [_slim_schema(s) for s in schema]
    if not isinstance(schema, dict):
        return schema
    out = {}
    for key, value in schema.items():
        if key == "title" and isinstance(value, str):
            continue
        if key == "default" and value is None:
            continue
        # "properties" maps names → schemas; a property literally called
        # "title" must survive, so recurse into each value, not the mapping keys.
        if key == "properties" and isinstance(value, dict):
            out[key] = {name: _slim_schema(sub) for name, sub in value.items()}
            continue
        out[key] = _slim_schema(value)
    variants = out.get("anyOf")
    if isinstance(variants, list):
        non_null = [v for v in variants if v != {"type": "null"}]
        if len(non_null) == 1 and len(non_null) < len(variants):
            del out["anyOf"]
            out = {**non_null[0], **out}
    return out


def toolsets_summary() -> list[dict[str, Any]]:
    """Overview of every known toolset, for the list_toolsets meta-tool."""
    summary = []
    for ts in sorted(_by_toolset):
        names = _by_toolset[ts]
        records = [_registry[n] for n in names]
        registered_count = sum(1 for r in records if r.registered)
        summary.append(
            {
                "name": ts,
                "tool_count": len(records),
                "read_only_tool_count": sum(1 for r in records if r.read_only),
                "write_tool_count": sum(1 for r in records if not r.read_only),
                "registered_tool_count": registered_count,
                "enabled": registered_count > 0,
                "fully_enabled": registered_count == len(records),
            }
        )
    return summary


def enable_toolset_by_name(toolset: str) -> dict[str, Any]:
    """Register every eligible tool in `toolset`. Used by the enable_toolset meta-tool."""
    if toolset not in _by_toolset:
        return {
            "error": f"Unknown toolset {toolset!r}.",
            "known_toolsets": sorted(_by_toolset),
        }
    newly_enabled = []
    already_enabled = []
    skipped_read_only = []
    for name in _by_toolset[toolset]:
        record = _registry[name]
        if auth.all_instances_read_only() and not record.read_only:
            skipped_read_only.append(name)
            continue
        if record.registered:
            already_enabled.append(name)
            continue
        _register(record)
        newly_enabled.append(name)
    return {
        "toolset": toolset,
        "newly_enabled_tools": newly_enabled,
        "already_enabled_tools": already_enabled,
        "skipped_read_only_tools": skipped_read_only,
    }


def register_meta_tools() -> None:
    """Expose list_toolsets/enable_toolset. Only called when dynamic mode is on."""

    @mcp.tool()
    def list_toolsets() -> Any:
        """List every Domo toolset (one per resource group, e.g. "datasets",
        "cards", "users"), its tool counts, and whether it's currently
        enabled. Call this first to discover what's available, then call
        enable_toolset with a name from this list to register its tools."""
        return format_result(toolsets_summary())

    @mcp.tool()
    async def enable_toolset(toolset: str, ctx: Context) -> Any:
        """Register all tools belonging to a Domo toolset for this session.

        Args:
            toolset: A toolset name returned by list_toolsets (e.g. "datasets").

        Tools that mutate Domo data are skipped while every configured
        instance is read-only (the default).
        """
        result = enable_toolset_by_name(toolset)
        try:
            await ctx.session.send_tool_list_changed()
        except Exception as exc:  # pragma: no cover - best-effort notification
            print(f"domo-mcp-server: tool list changed notification failed: {exc}", file=sys.stderr)
        return format_result(result)
