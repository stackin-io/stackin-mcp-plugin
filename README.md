<p align="center">
  <img src="assets/logo.png" alt="Stackin — Brazilian fiscal documents over MCP" width="120">
</p>

<h1 align="center">Stackin MCP plugin — NF-e and NFS-e for ChatGPT, Claude Code, Codex and Cursor</h1>

<p align="center">
  Issue, consult, correct and cancel Brazilian electronic invoices (<strong>nota fiscal eletrônica</strong>)
  from any AI client that speaks the Model Context Protocol.
</p>

<p align="center">
  <a href="https://github.com/stackin-io/stackin-mcp-plugin/blob/master/LICENSE"><img alt="MIT license" src="https://img.shields.io/github/license/stackin-io/stackin-mcp-plugin"></a>
  <a href="https://mcp.stackin.io/mcp"><img alt="MCP server" src="https://img.shields.io/badge/MCP-streamable--http-1f7a4d"></a>
  <a href="https://docs.stackin.io/mcp"><img alt="Documentation" src="https://img.shields.io/badge/docs-docs.stackin.io-informational"></a>
  <a href="https://app.stackin.io"><img alt="Get an API key" src="https://img.shields.io/badge/API%20key-app.stackin.io-black"></a>
</p>

---

Ask in plain language — *"issue an NFS-e for this service"*, *"why was my last NF-e rejected?"*,
*"cancel invoice 1042 and tell me the reason code"* — and the model does it through Stackin,
against SEFAZ and the municipal NFS-e webservices.

**Sixteen tools, nine skills, one hosted server.** No SDK to install, no XML to sign, no
certificate to juggle in the client.

- 🧾 **NF-e** (goods) and **NFS-e** (services) — issue, consult, cancel
- 🔎 **Diagnose a rejection** by the tax authority's own code, and choose reissue vs. correction
- ✉️ **Correction letter (CC-e)** against an authorized NF-e
- 📥 **Received invoices** — read and manifest documents other companies issued against yours
- 🔢 **Numbering invalidation** for a reserved, never-used NF-e range
- 📄 **DANFE / DANFSe PDF** straight out of the conversation
- 🔎 **Fiscal code lookup** — resolve an NCM, CFOP or CEST instead of guessing one, and confirm who a CNPJ belongs to

## Table of contents

- [Install in Claude Code](#install-in-claude-code)
- [Install in ChatGPT and Codex](#install-in-chatgpt-and-codex)
- [Connect from Cursor or any MCP client](#connect-from-cursor-or-any-mcp-client)
- [Authentication: OAuth or API key](#authentication-oauth-or-api-key)
- [Skills](#skills)
- [What is in this repository](#what-is-in-this-repository)
- [One plugin, three clients](#one-plugin-three-clients)
- [MCP Registry](#mcp-registry)
- [FAQ](#faq)
- [Maintainer notes](#maintainer-notes)

## Install in Claude Code

The repository is its own marketplace, so it installs straight from GitHub:

```bash
claude plugin marketplace add stackin-io/stackin-mcp-plugin
claude plugin install stackin@stackin
```

The plugin brings the nine skills and points Claude Code at `https://mcp.stackin.io/mcp`.
**There is nothing to configure**: the first tool call answers 401 with `WWW-Authenticate`,
and Claude Code follows it — run `/mcp` in the session, authorize in the browser that opens,
and the token is stored for you. The client registers itself through `/oauth/register`, so no
`client_id` is handed out by anyone.

Prefer a static key? Add the server by hand with a header instead of installing the plugin —
see [Authentication](#authentication-oauth-or-api-key).

## Install in ChatGPT and Codex

The same server is published as a ChatGPT app over Developer Mode. Enable developer mode,
register `https://mcp.stackin.io/mcp` as a connector, and authorize — the full walkthrough,
with video, is at [docs.stackin.io/mcp](https://docs.stackin.io/mcp).

## Connect from Cursor or any MCP client

Any MCP client can use the server directly, without this plugin. Cursor reads
`.cursor/mcp.json` in the project, or `~/.cursor/mcp.json`. **The interpolation syntax is not
the same as Claude Code's**: Cursor wants `${env:VAR}`.

```json
{
  "mcpServers": {
    "stackin": {
      "url": "https://mcp.stackin.io/mcp",
      "headers": { "Authorization": "Bearer ${env:STACKIN_API_KEY}" }
    }
  }
}
```

Claude Code, by hand — `${VAR}` expands from the environment:

```bash
claude mcp add --transport http stackin https://mcp.stackin.io/mcp \
  --header "Authorization: Bearer ${STACKIN_API_KEY}"
```

| Property | Value |
|---|---|
| Endpoint | `https://mcp.stackin.io/mcp` |
| Transport | `streamable-http` |
| Auth | OAuth 2.1 with PKCE and dynamic client registration, or a static Bearer key |
| Environments | Homologation and production, fixed on the key or on the authorized connection |

## Authentication: OAuth or API key

Two ways in, and they behave differently.

**An API key.** Generate one at [app.stackin.io](https://app.stackin.io); it already carries
the environment, so there is nothing to choose in the client. Send it as
`Authorization: Bearer <key>`.

**OAuth, with no key at all.** Leave the header out: a tool call answers 401 with
`WWW-Authenticate` pointing at `/.well-known/oauth-protected-resource`, which is what makes
Claude Code offer to log in when you run `/mcp`. The server supports dynamic client
registration (`/oauth/register`), so a client that registers itself gets a `client_id` without
anyone being asked. Cursor can also hold static client credentials under an `auth` key instead
of registering dynamically.

Verified on 2026-09-09, up to the browser: the server connects with no header at all, a tool
call answers 401 with the `resource_metadata` challenge, the protected-resource document
resolves, `/oauth/register` returns 201 and `/oauth/authorize` redirects to the consent
screen. **The browser leg itself has not been walked from Claude Code or Cursor** — ChatGPT
completed a real consent, those two have not. If one stops midway, look at the `redirect_uri`
it uses: `/oauth/authorize` only accepts a URI the client registered.

## Skills

A skill exists only where the order of operations, or a fiscal rule, adds something a tool
description cannot carry on its own.

| Skill | What it carries |
|---|---|
| `issue-invoice` | Which document the situation needs, and validating before issuing |
| `consult-invoice` | Finding a document, and which identifier each operation takes |
| `cancel-invoice` | Confirming before an irreversible act, and when a correction letter is the right tool instead |
| `diagnose-invoice` | Reading the tax authority's own rejection code, and choosing between reissue and correction |
| `correct-invoice` | Filing a correction letter against an authorized NF-e, and what a CC-e may not change |
| `invalidate-numbering` | Declaring an NF-e numbering range reserved and never used |
| `received-invoices` | Reading documents other companies issued against this one, and answering them |
| `fiscal-lookup` | Resolving an NCM, CFOP or CEST before issuing, instead of guessing one |
| `taxpayer-lookup` | Confirming who a tax id belongs to, and why a 404 is not an invalid CNPJ |

## What is in this repository

This repository is the **distribution layer**: the manifests, the skills and the assets. The
server itself lives at `https://mcp.stackin.io/mcp` and speaks the Model Context Protocol.

| Path | What it is |
|---|---|
| `.codex-plugin/plugin.json` | Plugin identity, version, category, legal links |
| `.app.json` | Maps the plugin to the registered MCP connection |
| `.agents/plugins/marketplace.json` | Local marketplace, for installing before publishing |
| `.claude-plugin/plugin.json` | Plugin identity for Claude Code |
| `.claude-plugin/marketplace.json` | This repository as a marketplace Claude Code can add |
| `.mcp.json` | The hosted MCP server, for Claude Code |
| `server.json` | The MCP Registry entry |
| `skills/` | The nine workflows that need more than a tool description |
| `assets/` | Icon and logo |

## One plugin, three clients

The repo carries three manifests because three ecosystems look in three places, and each one
fails silently when its file is missing:

| Client | Looks for | What it reads |
|---|---|---|
| ChatGPT / Codex | `.codex-plugin/plugin.json` + `.app.json` | the app id and the hosted MCP |
| Codex marketplace | `.agents/plugins/marketplace.json` | this repo as a source |
| Claude Code | `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json`, `.mcp.json` | the skills and `https://mcp.stackin.io/mcp` |

Adding the folder to Claude Code failed with *"No marketplace manifest found …
(expected .cursor-plugin/marketplace.json or .claude-plugin/marketplace.json)"* until the
third row existed. The skills are shared: all three point at `skills/`, so a skill written
once is read by every client.

## MCP Registry

`server.json` describes the hosted server for the
[official MCP Registry](https://registry.modelcontextprotocol.io) as a remote entry —
`io.github.stackin-io/stackin`, `streamable-http`, no package to install.

Publishing is automated: pushing a `v*` tag runs `.github/workflows/publish-mcp.yml`, which
stamps the version from the tag, authenticates with **GitHub OIDC** (no stored token — the
workflow's own identity is what grants the `io.github.stackin-io/*` namespace) and publishes.

```bash
git tag v1.0.0 && git push origin v1.0.0
```

The registry lists the *public* repository, which is why the entry lives here and not beside
the server's own source.

## FAQ

**Do I need a digital certificate (A1/A3) in the client?** No. The certificate is uploaded
once at [app.stackin.io](https://app.stackin.io) and stays server-side.

**Does it work in production, or only homologation?** Both. The environment is fixed on the
API key, or on the connection you authorized over OAuth — there is nothing to pick per call.

**Which municipalities are supported for NFS-e?** The ones Stackin covers; consult
[docs.stackin.io](https://docs.stackin.io). NF-e is nationwide through SEFAZ.

**Can I use the server without this plugin?** Yes — it is a plain MCP server. The plugin only
adds the skills and saves you the manual configuration.

**Is it free?** Issuing consumes credits from your Stackin account. Consulting and cancelling
do not.

**Why do the code lookups answer 403 on my connection?** Because it was made over OAuth.
`lookup_fiscal_code`, `search_fiscal_codes`, `list_fiscal_kinds` and `lookup_taxpayer` are
the four tools the API maps to no scope, so an authorized app is refused no matter what it
was granted — reconnecting will not change it. They work when the connection carries the
company's own API key.

**A CNPJ I know is valid comes back 404 from `lookup_taxpayer`. Is it wrong?** Probably not.
That registry reloads monthly from the Receita Federal's dump, so a company registered in
the last few weeks is not in it yet. It is not a validity check, and nothing should block an
invoice over it.

## Maintainer notes

`app_id` in `.app.json` was filled on 2026-09-06, once `mcp.stackin.io` was registered in
OpenAI Developer Mode and a real connector completed the OAuth authorisation. It was left
empty until then on purpose — it is the one value that cannot be prepared ahead of time.

**A stale tool list was fixed by creating a new app, not by rescanning.** The first app
(`asdk_app_6a9d458d…`) had been scanned before the NFS-e restriction and kept advertising the
old surface. `.app.json` now names the second one; if a third is ever created, this file is
the thing to update, and nothing warns you when it is wrong.

**NF-e came back on 2026-09-07, in two steps.** First `document_type` widened to accept `nfe`
on the existing eight tools — a change the count could not reveal. Then the four NF-e-only
operations came back: `correct_invoice`, `invalidate_numbering`, `list_received_invoices` and
`manifest_received_invoice`. **Twelve tools then**, seven skills.

**The four lookup tools landed on 2026-09-10**: `lookup_fiscal_code`,
`search_fiscal_codes`, `list_fiscal_kinds` and `lookup_taxpayer`, with the
`fiscal-lookup` and `taxpayer-lookup` skills. **Sixteen tools now**, nine skills. They are the first tools
here an OAuth connection cannot use at all — the API maps their routes to no scope,
so only a company's own API key reaches them, and reconnecting does not change that.

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
now reports **Authorization used: OAuth**, so it says `oauth`. The enum for that field is not
in OpenAI's published documentation — `developers.openai.com/codex/plugins/apps.md` redirects
to a 404 — so this is the honest description rather than a verified value. If the submission
rejects it, that is where to look first.

## License

MIT — see [LICENSE](LICENSE).
