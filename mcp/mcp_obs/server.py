"""Stdio MCP server exposing observability operations as typed tools."""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Awaitable, Callable
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from mcp_obs.client import VictoriaLogsClient, VictoriaTracesClient

server = Server("obs")

# ---------------------------------------------------------------------------
# Input models
# ---------------------------------------------------------------------------


class _NoArgs(BaseModel):
    """Empty input model for tools that only need server-side configuration."""


class _LogsSearch(BaseModel):
    query: str = Field(
        default="*", description="LogsQL query (e.g., 'severity:ERROR', 'backend')"
    )
    limit: int = Field(default=10, ge=1, le=100, description="Max entries to return")
    time_range: str = Field(
        default="1h", description="Time range (e.g., '1h', '24h', '7d')"
    )


class _ErrorCount(BaseModel):
    service: str = Field(default="", description="Filter by service name (optional)")
    time_range: str = Field(
        default="1h", description="Time window (e.g., '1h', '24h', '7d')"
    )


class _TracesList(BaseModel):
    service: str = Field(default="", description="Filter by service name (optional)")
    limit: int = Field(default=10, ge=1, le=50, description="Max traces to return")
    time_range: str = Field(
        default="1h", description="Time range (e.g., '1h', '24h', '7d')"
    )


class _TraceGet(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _logs_client() -> VictoriaLogsClient:
    url = os.environ.get("VICTORIALOGS_URL", "http://localhost:42010")
    return VictoriaLogsClient(url)


def _traces_client() -> VictoriaTracesClient:
    url = os.environ.get("VICTORIATRACES_URL", "http://localhost:42011")
    return VictoriaTracesClient(url)


def _text(data: BaseModel | list | dict) -> list[TextContent]:
    """Serialize data to JSON text block."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False))]


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------


async def _logs_search(args: _LogsSearch) -> list[TextContent]:
    """Search logs by query and time range."""
    entries = await _logs_client().search(
        query=args.query, limit=args.limit, time_range=args.time_range
    )
    return _text({"entries": [e.model_dump() for e in entries], "count": len(entries)})


async def _logs_error_count(args: _ErrorCount) -> list[TextContent]:
    """Count errors per service over a time window."""
    counts = await _logs_client().error_count(
        service=args.service, time_range=args.time_range
    )
    return _text({"error_counts": counts, "time_range": args.time_range})


async def _traces_list(args: _TracesList) -> list[TextContent]:
    """List recent traces for a service."""
    traces = await _traces_client().list_traces(
        service=args.service, limit=args.limit, time_range=args.time_range
    )
    return _text({"traces": [t.model_dump() for t in traces], "count": len(traces)})


async def _traces_get(args: _TraceGet) -> list[TextContent]:
    """Fetch a specific trace by ID."""
    trace = await _traces_client().get_trace(args.trace_id)
    if trace is None:
        return _text({"error": f"Trace not found: {args.trace_id}"})
    return _text(trace.model_dump())


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

_Registry = tuple[type[BaseModel], Callable[..., Awaitable[list[TextContent]]], Tool]

_TOOLS: dict[str, _Registry] = {}


def _register(
    name: str,
    description: str,
    model: type[BaseModel],
    handler: Callable[..., Awaitable[list[TextContent]]],
) -> None:
    schema = model.model_json_schema()
    schema.pop("$defs", None)
    schema.pop("title", None)
    _TOOLS[name] = (
        model,
        handler,
        Tool(name=name, description=description, inputSchema=schema),
    )


_register(
    "logs_search",
    "Search VictoriaLogs using LogsQL query. Use 'severity:ERROR' for errors, or any keyword.",
    _LogsSearch,
    _logs_search,
)
_register(
    "logs_error_count",
    "Count errors per service over a time window. Returns a dict of service -> error count.",
    _ErrorCount,
    _logs_error_count,
)
_register(
    "traces_list",
    "List recent traces from VictoriaTraces. Optionally filter by service name.",
    _TracesList,
    _traces_list,
)
_register(
    "traces_get",
    "Fetch a specific trace by ID. Returns full trace with all spans.",
    _TraceGet,
    _traces_get,
)


# ---------------------------------------------------------------------------
# MCP handlers
# ---------------------------------------------------------------------------


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [entry[2] for entry in _TOOLS.values()]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    entry = _TOOLS.get(name)
    if entry is None:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    model_cls, handler, _ = entry
    try:
        args = model_cls.model_validate(arguments or {})
        return await handler(args)
    except Exception as exc:
        return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
