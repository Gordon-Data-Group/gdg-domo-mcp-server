"""Toolset registry and lazy tool registration for the Domo MCP server.

Every domain tool module (src/tools/*.py) registers its tools through the
`domo_tool` decorator defined here instead of calling `@mcp.tool()`
directly. That indirection is what makes two things possible:

1. DOMO_READ_ONLY (default "1" — read-only): tools tagged `read_only=False`
   are simply never attached to the server unless an operator explicitly
   sets DOMO_READ_ONLY=0. This is belt-and-suspenders with the enforcement
   in src/auth.py, which blocks mutating HTTP verbs outright — so even a
   mis-tagged tool can't reach a write endpoint.

2. DOMO_DYNAMIC_TOOLSETS (default "0" — off): when enabled, domain tools are
   *not* registered at startup. Only two meta-tools are exposed —
   `list_toolsets` and `enable_toolset` — and calling `enable_toolset`
   registers that group's tools on demand. This keeps the initial tool
   list (and its token cost) tiny for sessions that only need a few
   toolsets out of the ~35 available. DOMO_DEFAULT_TOOLSETS (comma-separated)
   can pre-enable specific toolsets at startup even in dynamic mode.

Every tool module must still be *imported* unconditionally (see
src/server.py) so its `domo_tool`-decorated functions run and populate the
registry below — dynamic mode defers *registration*, not *import*, which is
cheap (no I/O, just function definitions).
"""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable

from mcp.server.fastmcp import Context
from mcp.types import ToolAnnotations

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

        if auth.read_only_mode() and not read_only:
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
        record.func,
        name=record.name,
        annotations=ToolAnnotations(readOnlyHint=record.read_only),
    )
    record.registered = True


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
        if auth.read_only_mode() and not record.read_only:
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
        return toolsets_summary()

    @mcp.tool()
    async def enable_toolset(toolset: str, ctx: Context) -> Any:
        """Register all tools belonging to a Domo toolset for this session.

        Args:
            toolset: A toolset name returned by list_toolsets (e.g. "datasets").

        Tools that mutate Domo data are skipped while DOMO_READ_ONLY is
        enabled (the default) — set DOMO_READ_ONLY=0 to allow them.
        """
        result = enable_toolset_by_name(toolset)
        try:
            await ctx.session.send_tool_list_changed()
        except Exception as exc:  # pragma: no cover - best-effort notification
            print(f"domo-mcp-server: tool list changed notification failed: {exc}", file=sys.stderr)
        return result
