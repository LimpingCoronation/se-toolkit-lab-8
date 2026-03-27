#!/usr/bin/env python3
"""
Entrypoint for running nanobot gateway in Docker.

Resolves environment variables into the config at runtime,
then launches `nanobot gateway`.
"""

import json
import os
import sys


def resolve_config():
    """Read config.json, inject env var values, write resolved config."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    workspace_path = os.path.join(os.path.dirname(__file__), "workspace")

    with open(config_path, "r") as f:
        config = json.load(f)

    # Resolve LLM provider API key and base URL from env vars
    if "providers" in config and "custom" in config["providers"]:
        if llm_api_key := os.environ.get("LLM_API_KEY"):
            config["providers"]["custom"]["apiKey"] = llm_api_key
        if llm_api_base := os.environ.get("LLM_API_BASE_URL"):
            config["providers"]["custom"]["apiBase"] = llm_api_base

    # Resolve MCP server environment variables
    if "tools" in config and "mcpServers" in config["tools"]:
        if "lms" in config["tools"]["mcpServers"]:
            lms_config = config["tools"]["mcpServers"]["lms"]
            if "env" not in lms_config:
                lms_config["env"] = {}
            if backend_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
                lms_config["env"]["NANOBOT_LMS_BACKEND_URL"] = backend_url
            if api_key := os.environ.get("NANOBOT_LMS_API_KEY"):
                lms_config["env"]["NANOBOT_LMS_API_KEY"] = api_key

    # Write resolved config to a temp file
    resolved_path = os.path.join(os.path.dirname(__file__), "config.resolved.json")
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    return resolved_path, workspace_path


def main():
    resolved_config, workspace = resolve_config()

    # Launch nanobot gateway
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_config, "--workspace", workspace])


if __name__ == "__main__":
    main()
