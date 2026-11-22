# Changelog

## v1.5.0 — 2026-11-22

### Features
- **skills:** fiscal-lookup simulates IBS/CBS with calculate_ibs_cbs (stackin-mcp#57)
- **skills:** manage-items, and issue-invoice and fiscal-lookup use the catalog (stackin-io/stackin-api#642)

### Docs
- **readme:** forty-one tools, items catalog and IBS/CBS simulation live (stackin-mcp#57)
- **readme:** fiscal-lookup row names calculate_ibs_cbs (stackin-mcp#57)
- **readme:** forty tools, fourteen skills, the items catalog (stackin-io/stackin-api#642)

### Build
- **manifests:** version 1.5.0 (stackin-mcp#57)

### Chores
- merge items catalog skills (#15) into feature/57

## v1.4.0 — 2026-11-21

### Features
- **skills:** first-invoice from readiness to production (stackin-mcp#45)

### Bug Fixes
- **skills:** first-invoice resolves the registry city to a name, not an IBGE code (stackin-mcp#45)

### Docs
- **readme:** thirteen skills in the install and layout sections (stackin-mcp#45)
- **manifests:** GEMINI.md lists first-invoice and the readiness rule (stackin-mcp#45)
- **readme:** thirty-five tools, thirteen skills, update_company (stackin-mcp#45)
- **skills:** company:write in the permissions select-company reads (stackin-mcp#45)
- **skills:** issue-invoice completes the company with update_company, readiness once (stackin-mcp#45)
- drop the response-time promise from the security policy
- add a security policy with a reporting contact (#11)

### Build
- **manifests:** version 1.4.0 (stackin-mcp#45)

### Chores
- **gitignore:** block certificate, key and .env files (stackin-io/devops#47)
- **assets:** add a 400x400 logo for marketplace listings

## v1.3.0 — 2026-11-20

### Features
- **skills:** manage-webhooks for list, create, delete and deliveries (#8)
- **manifests:** Cursor plugin over the shared skills (#8)
- **manifests:** Gemini CLI extension over the shared skills (#8)

### Bug Fixes
- **manifests:** point logoDark at logo-dark.png (#8)
- **manifests:** restore the ChatGPT app id Codex reads (#8)
- **skills:** drop pending from the list_invoices status filter (#6)

### Docs
- **manifests:** GEMINI.md lists manage-webhooks and the suggestion rules (#8)
- **readme:** thirty-four tools, twelve skills, the v0.9.0 surface (#8)
- **skills:** webhook:manage granted on demand, search_cities takes no company (#8)
- **skills:** invoice_stats for counts, billing and rejection trend (#8)
- **skills:** list_invalidations before declaring a range (#8)
- **skills:** classify_item as a suggestion confirmed by the person (#8)
- **skills:** readiness before the first document, search_cities, discount, issued_at, contingency (#8)
- **skills:** explain_rejection after the submissions, suggested and transient (#8)
- **readme:** install per client, five manifests, OAuth walked from Claude Code (#8)

### Build
- **manifests:** version 1.3.0 (#8)

### CI
- **manifests:** fail on an empty app id, a missing asset or a version split (#8)

## v1.2.0 — 2026-11-18

### Docs
- **readme:** twenty-four tools, received billing in the FAQ (#4)
- **skills:** deactivate and reactivate clients, inactive listing (#4)
- **skills:** received invoices billing, on-demand sync and the one-hour wait (#4)

### Build
- **manifests:** version 1.2.0 (#4)

## v1.1.0 — 2026-11-17

### Features
- **skills:** select-company for list_authorized_companies (#2)
- **skills:** manage-clients for list_clients, get_client and save_client (#2)

### Docs
- **manifests:** name the client registry and company selection (#2)
- **readme:** twenty tools, eleven skills, client registry and company selection (#2)
- **skills:** list_invoices leaves item lines out unless include_items (#2)
- **skills:** send a confirmed taxpayer to the client registry (#2)
- **skills:** look the recipient up with list_clients before issuing (#2)

### Build
- **manifests:** version 1.1.0 (#2)

### Chores
- **platform:** install action-platform
