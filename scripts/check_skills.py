"""Fails when the skills and the live server disagree about the tools.

Two repositories describing one product drift silently: a tool ships on the
server and no skill mentions it, or a skill keeps naming one that was removed.
This turns that into a red build instead of something a reviewer finds.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
import urllib.request

ENDPOINT = "https://mcp.stackin.io/mcp"
SKILLS = pathlib.Path("skills")


def live_tools() -> set[str]:
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    ).encode()
    request = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read())
    return {tool["name"] for tool in payload["result"]["tools"]}


def mentioned_tools() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        names = set(re.findall(r"`?\b([a-z]+(?:_[a-z]+)+)\b`?", path.read_text()))
        found[path.parent.name] = names
    return found


def main() -> int:
    tools = live_tools()
    per_skill = mentioned_tools()
    named = set().union(*per_skill.values()) if per_skill else set()

    invented = {name for name in named if name.endswith("_invoice")} - tools
    invented |= {
        name
        for name in named
        if name.startswith(("list_", "get_", "issue_", "cancel_", "correct_"))
    } - tools
    uncovered = tools - named

    if invented:
        print(f"skills name tools the server does not have: {sorted(invented)}")
    if uncovered:
        print(f"tools no skill mentions: {sorted(uncovered)}")

    print(f"{len(tools)} tools live, {len(per_skill)} skills")
    return 1 if invented or uncovered else 0


if __name__ == "__main__":
    raise SystemExit(main())
