"""Async HTTP client for VictoriaLogs and VictoriaTraces APIs."""

import httpx
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class LogEntry(BaseModel):
    """A single log entry from VictoriaLogs."""

    timestamp: str
    severity: str
    event: str
    service: str
    trace_id: str = ""
    span_id: str = ""
    message: str = ""
    error: str = ""


class TraceSummary(BaseModel):
    """Summary of a trace from VictoriaTraces."""

    trace_id: str
    service: str
    operation: str
    duration_ms: int
    span_count: int
    has_error: bool


class TraceDetail(BaseModel):
    """Detailed trace with spans."""

    trace_id: str
    service: str
    duration_ms: int
    has_error: bool
    spans: list[dict]


# ---------------------------------------------------------------------------
# VictoriaLogs client
# ---------------------------------------------------------------------------


class VictoriaLogsClient:
    """Client for VictoriaLogs HTTP API."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=30.0)

    async def search(
        self, query: str = "*", limit: int = 10, time_range: str = "1h"
    ) -> list[LogEntry]:
        """Search logs using LogsQL query."""
        import json

        async with self._client() as c:
            try:
                # VictoriaLogs query API
                url = f"{self.base_url}/select/logsql/query"
                params = {"query": query, "limit": limit}
                if time_range:
                    params["time"] = time_range

                r = await c.get(url, params=params)
                r.raise_for_status()

                # VictoriaLogs returns newline-delimited JSON
                lines = r.text.strip().split("\n")
                entries = []
                for line in lines:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            entries.append(
                                LogEntry(
                                    timestamp=data.get("_time", ""),
                                    severity=data.get("severity", ""),
                                    event=data.get("event", ""),
                                    service=data.get("service.name", ""),
                                    trace_id=data.get("trace_id", ""),
                                    span_id=data.get("span_id", ""),
                                    message=data.get("_msg", ""),
                                    error=data.get("error", ""),
                                )
                            )
                        except json.JSONDecodeError:
                            continue
                return entries
            except httpx.ConnectError:
                return []
            except Exception:
                return []

    async def error_count(
        self, service: str = "", time_range: str = "1h"
    ) -> dict[str, int]:
        """Count errors per service over a time window."""
        async with self._client() as c:
            try:
                query = "severity:ERROR"
                if service:
                    query = f'service.name:"{service}" AND severity:ERROR'

                url = f"{self.base_url}/select/logsql/query"
                params = {"query": query, "time": time_range, "limit": 1000}

                r = await c.get(url, params=params)
                r.raise_for_status()

                # Count errors by service
                error_counts: dict[str, int] = {}
                lines = r.text.strip().split("\n")
                for line in lines:
                    if line.strip():
                        import json

                        data = json.loads(line)
                        svc = data.get("service.name", "unknown")
                        error_counts[svc] = error_counts.get(svc, 0) + 1

                return error_counts
            except Exception:
                return {}


# ---------------------------------------------------------------------------
# VictoriaTraces client
# ---------------------------------------------------------------------------


class VictoriaTracesClient:
    """Client for VictoriaTraces HTTP API (native format)."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=30.0)

    async def list_traces(
        self, service: str = "", limit: int = 10, time_range: str = "1h"
    ) -> list[TraceSummary]:
        """List recent traces for a service."""
        async with self._client() as c:
            try:
                # VictoriaTraces native API for trace search
                url = f"{self.base_url}/api/traces"
                params = {"limit": limit}
                if service:
                    params["service"] = service

                r = await c.get(url, params=params)
                r.raise_for_status()

                data = r.json()
                traces = []
                for t in data.get("data", []):
                    traces.append(
                        TraceSummary(
                            trace_id=t.get("traceID", ""),
                            service=t.get("serviceName", ""),
                            operation=t.get("operationName", ""),
                            duration_ms=int(t.get("duration", 0) / 1_000_000),
                            span_count=len(t.get("spans", [])),
                            has_error=any(
                                s.get("tags", {}).get("error", False)
                                for s in t.get("spans", [])
                            ),
                        )
                    )
                return traces
            except Exception:
                return []

    async def get_trace(self, trace_id: str) -> TraceDetail | None:
        """Fetch a specific trace by ID."""
        async with self._client() as c:
            try:
                url = f"{self.base_url}/api/traces/{trace_id}"
                r = await c.get(url)
                r.raise_for_status()

                data = r.json()
                if not data.get("data"):
                    return None

                t = data["data"][0]
                spans = []
                for s in t.get("spans", []):
                    spans.append(
                        {
                            "span_id": s.get("spanID", ""),
                            "operation": s.get("operationName", ""),
                            "service": s.get("serviceName", ""),
                            "duration_ms": int(s.get("duration", 0) / 1_000_000),
                            "tags": s.get("tags", []),
                        }
                    )

                return TraceDetail(
                    trace_id=t.get("traceID", ""),
                    service=t.get("serviceName", ""),
                    duration_ms=int(t.get("duration", 0) / 1_000_000),
                    has_error=any(
                        s.get("tags", {}).get("error", False) for s in t.get("spans", [])
                    ),
                    spans=spans,
                )
            except Exception:
                return None
