# Observability Skills

You have access to the system's observability data through VictoriaLogs and VictoriaTraces MCP tools. This skill guide teaches you how to investigate system health and diagnose issues.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `logs_search` | Search VictoriaLogs using LogsQL query | `query` (default "*"), `limit` (default 10), `time_range` (default "1h") |
| `logs_error_count` | Count errors per service over a time window | `service` (optional), `time_range` (default "1h") |
| `traces_list` | List recent traces from VictoriaTraces | `service` (optional), `limit` (default 10), `time_range` (default "1h") |
| `traces_get` | Fetch a specific trace by ID | `trace_id` (required) |

## LogsQL Query Syntax

VictoriaLogs uses LogsQL for querying:

- `*` — All logs
- `severity:ERROR` — Only error logs
- `service.name:"Learning Management Service"` — Filter by service
- `event:db_query` — Filter by event type
- `severity:ERROR AND service.name:"Learning Management Service"` — Combine filters

## How to Use These Tools

### When the user asks about errors

1. **Start with `logs_error_count`** to get an overview of errors by service
2. **Use `logs_search`** with `query="severity:ERROR"` to see recent error details
3. **If you find a trace_id in the logs**, use `traces_get` to fetch the full trace

### When the user asks about system health

1. Check `logs_error_count` for the last hour
2. If there are errors, use `logs_search` to investigate
3. Summarize findings concisely — don't dump raw JSON

### When investigating a specific issue

1. Search logs for the relevant keyword or event
2. Note any trace_id values in the log entries
3. Fetch the full trace with `traces_get` to see the complete request flow
4. Look for spans with `error: true` tags

## Response Guidelines

- **Lead with the answer**: "Found 3 errors in the last hour, all from the Learning Management Service"
- **Summarize, don't dump**: Extract key information from logs/traces, don't paste raw JSON
- **Include trace context**: When relevant, mention trace_id for further investigation
- **Offer follow-up**: "Would you like me to fetch the full trace for any of these errors?"

## Example Interactions

### User: "Any errors in the last hour?"

1. Call `logs_error_count` with `time_range="1h"`
2. If errors found, call `logs_search` with `query="severity:ERROR"` and `limit=5`
3. Respond with:
   > Found 2 errors in the last hour:
   > - Learning Management Service: 2 errors
   >
   > Most recent error: `db_query` failed with "connection refused" at 11:07:38
   > Trace ID: `e228cd3b6290cdab267ca187be64492d`
   >
   > This appears to be a database connectivity issue. Would you like me to fetch the full trace?

### User: "Show me recent logs for the backend"

Call `logs_search` with `query='service.name:"Learning Management Service"'` and `limit=10`.

### User: "What went wrong with request XYZ?"

If the user provides a trace_id:
1. Call `traces_get` with the trace_id
2. Analyze the span hierarchy to find where the error occurred
3. Explain which service/span failed and why

## Important Notes

- VictoriaLogs stores structured logs from all instrumented services
- VictoriaTraces stores distributed traces showing request flows across services
- Each log entry may include a `trace_id` that links to a full trace
- The service name in our system is "Learning Management Service"
- If a tool returns empty results, try expanding the time_range (e.g., "24h" instead of "1h")
