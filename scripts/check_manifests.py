"""Fails when a manifest is malformed in a way its client would ignore silently.

Every client here skips a bad manifest without an error. Codex drops an app
whose `id` is empty with a log warning and nothing else, which is how the
ChatGPT app declaration went missing for two months. This turns those cases
into a red build.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_ID = re.compile(r"^asdk_app_[0-9a-f]{32}$")
MANIFESTS = [
    ".app.json",
    ".mcp.json",
    "server.json",
    "gemini-extension.json",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
]
VERSIONED = [
    "server.json",
    "gemini-extension.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
]


def load(relative: str, errors: list[str]) -> dict | None:
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"{relative}: missing")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as error:
        errors.append(f"{relative}: invalid JSON ({error})")
        return None


def check_apps(data: dict, errors: list[str]) -> None:
    apps = data.get("apps")
    if not isinstance(apps, dict) or not apps:
        errors.append(".app.json: `apps` must be a non-empty object keyed by app name")
        return
    for name, app in apps.items():
        app_id = (app or {}).get("id", "")
        if not APP_ID.match(app_id.strip()):
            errors.append(
                f".app.json: apps.{name}.id is {app_id!r}; Codex drops an app "
                "without a valid asdk_app_ id, silently"
            )


def check_paths(relative: str, data: dict, errors: list[str]) -> None:
    base = (ROOT / relative).parent.parent
    interface = data.get("interface", {})
    for key in ("composerIcon", "logo", "logoDark"):
        value = interface.get(key) or (data.get(key) if relative.startswith(".cursor") else None)
        if value and not (base / value).is_file():
            errors.append(f"{relative}: {key} points at missing file {value}")
    for key in ("skills", "apps", "mcpServers"):
        value = data.get(key)
        if isinstance(value, str) and not (base / value).exists():
            errors.append(f"{relative}: {key} points at missing path {value}")


def main() -> int:
    errors: list[str] = []
    loaded = {name: load(name, errors) for name in MANIFESTS}

    if loaded[".app.json"] is not None:
        check_apps(loaded[".app.json"], errors)

    for name in (".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"):
        if loaded[name] is not None:
            check_paths(name, loaded[name], errors)

    gemini = loaded["gemini-extension.json"]
    if gemini is not None:
        context = gemini.get("contextFileName", "GEMINI.md")
        if not (ROOT / context).is_file():
            errors.append(f"gemini-extension.json: contextFileName {context} is missing")

    versions = {
        name: loaded[name].get("version") for name in VERSIONED if loaded[name] is not None
    }
    if len(set(versions.values())) > 1:
        errors.append(f"versions disagree: {versions}")

    for error in errors:
        print(error)
    print(f"{len(MANIFESTS)} manifests, version {sorted(set(versions.values()))}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
