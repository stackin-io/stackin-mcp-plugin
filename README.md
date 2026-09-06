<p align="center">
  <img src="assets/logo.png" alt="stackin" width="120">
</p>

<h1 align="center">Stackin plugin</h1>

<p align="center">
  Brazilian fiscal documents in ChatGPT and Codex, over the hosted Stackin MCP server.
</p>

---

Ask in plain language — "issue an NFS-e for this service", "why was my last NF-e rejected?" —
and the model does it through Stackin.

This repository is the **distribution layer**: the manifest, the skills and the assets. The
server itself lives at `https://mcp.stackin.io/mcp` and speaks the Model Context Protocol;
any MCP client can use it directly, without this plugin.

## What is here

| Path | What it is |
|---|---|
| `.codex-plugin/plugin.json` | Plugin identity, version, category, legal links |
| `.app.json` | Maps the plugin to the registered MCP connection |
| `.agents/plugins/marketplace.json` | Local marketplace, for installing before publishing |
| `skills/` | The four workflows that need more than a tool description |
| `assets/` | Icon and logo |

## Skills

A skill exists only where the order of operations, or a fiscal rule, adds something a tool
description cannot carry on its own.

| Skill | What it carries |
|---|---|
| `issue-invoice` | Which document the situation needs, and validating before issuing |
| `consult-invoice` | Finding a document, and which identifier each operation takes |
| `cancel-invoice` | Confirming before an irreversible act, and when a correction letter is the right tool instead |
| `diagnose-invoice` | Reading the tax authority's own rejection code, and choosing between reissue and correction |

## Using the server without the plugin

```json
{
  "mcpServers": {
    "stackin": {
      "type": "http",
      "url": "https://mcp.stackin.io/mcp",
      "headers": { "Authorization": "Bearer your-key" }
    }
  }
}
```

Get a key at [app.stackin.io](https://app.stackin.io).

## One plugin, three clients

The repo carries three manifests because three ecosystems look in three
places, and each one fails silently when its file is missing:

| Client | Looks for | What it reads |
|---|---|---|
| ChatGPT / Codex | `.codex-plugin/plugin.json` + `.app.json` | the app id and the hosted MCP |
| Codex marketplace | `.agents/plugins/marketplace.json` | this repo as a source |
| Claude Code | `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `.mcp.json` | the skills and `https://mcp.stackin.io/mcp` |

Adding the folder to Claude Code failed with *"No marketplace manifest found …
(expected .cursor-plugin/marketplace.json or .claude-plugin/marketplace.json)"*
until the third row existed. The skills are shared: all three point at
`skills/`, so a skill written once is read by every client.

## Before publishing

`app_id` in `.app.json` was filled on 2026-09-06, once `mcp.stackin.io` was registered in
OpenAI Developer Mode and a real connector completed the OAuth authorisation. It was left
empty until then on purpose — it is the one value that cannot be prepared ahead of time.

**A stale tool list was fixed by creating a new app, not by rescanning.** The first app
(`asdk_app_6a9d458d…`) had been scanned before the NFS-e restriction and kept advertising the
old surface. `.app.json` now names the second one; if a third is ever created, this file is
the thing to update, and nothing warns you when it is wrong.

**The connector caches the tool list from the moment it was scanned.** The app was authorized
at 10:48 on 2026-09-06 and the NFS-e restriction went live at 12:00, so ChatGPT kept
advertising eleven tools — including three the server no longer has. Publishing a new plugin
version and running **Scan Tools** is what refreshes it; the fix is not on the server, which
was already correct. Check the count before testing anything: the server is the truth, and
`scripts/check_skills.py` reads it live.

**Read the identifier off the connector page, not out of the URL.** The address is
`chatgpt.com/plugins/plugin_asdk_app_…`, and `plugin_` there is part of the route, not of the
id. The page's own "App ID" field is the value that belongs here — `asdk_app_…`. Getting that
wrong is silent: nothing validates it until a submission fails.

`mcp.authentication` was `bearer`, written before the server spoke OAuth. The connector page
now reports **Authorization used: OAuth**, so it says `oauth`. The enum for that field is not in
OpenAI's published documentation — `developers.openai.com/codex/plugins/apps.md` redirects to a
404 — so this is the honest description rather than a verified value. If the submission rejects
it, that is where to look first.

## License

MIT — see [LICENSE](LICENSE).
