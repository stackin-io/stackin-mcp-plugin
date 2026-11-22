# Stackin

The `stackin` MCP server issues, consults, corrects and cancels Brazilian fiscal documents:
**NF-e** for goods and **NFS-e** for services. Every amount is in BRL. The first tool call
answers 401 and Gemini CLI runs the OAuth flow; `/mcp auth stackin` repeats it.

The workflows live in `skills/`, and Gemini CLI loads them from there. Each one carries what a
tool description cannot: the order of operations or a fiscal rule.

| Skill | Use it to |
|---|---|
| `issue-invoice` | Issue an NF-e or NFS-e, checking the company is ready and the data before it reaches the tax authority |
| `first-invoice` | Take a new company to its first document: readiness, `update_company`, a homologation test, then production |
| `consult-invoice` | Find a document and report its state; count and compare with `invoice_stats` |
| `diagnose-invoice` | Explain a rejection with `explain_rejection` and the authority's own answer, and what has to change |
| `cancel-invoice` | Cancel an authorized document, or file a correction letter when that is what is needed |
| `correct-invoice` | File a correction letter (CC-e) against an authorized NF-e |
| `invalidate-numbering` | Check `list_invalidations`, then declare a reserved, never-used NF-e range |
| `received-invoices` | Read NF-e other companies issued against this one, and file the company's position |
| `fiscal-lookup` | Resolve an NCM, CFOP or CEST before it goes on a document; `classify_item` only suggests; `calculate_ibs_cbs` simulates IBS/CBS |
| `taxpayer-lookup` | Confirm who a tax id belongs to before invoicing them |
| `manage-clients` | Find, read, save and fix the company's saved clients |
| `manage-items` | Find, read, save and fix the company's catalog of products and services |
| `select-company` | Pick which company a call acts for when one connection covers several |
| `manage-webhooks` | Register, list and remove webhook endpoints, and check whether deliveries arrive |

## Rules that apply to every call

- An issued document is legally binding. Confirm the data with the user; never infer it.
- An NF-e needs an `ncm` and a `cfop` on every item and a complete recipient address. Never
  guess either code: look it up with `fiscal-lookup`.
- Correction letters, numbering invalidation and recipient manifestations are NF-e only. A
  wrong NFS-e is cancelled and issued again.
- Look the recipient up with `list_clients` and pass its id as `client_id` before typing one
  into `issue_invoice`.
- When one connection covers several companies, every call that touches a company's documents
  needs `company_id` or `company_tax_id`; `list_authorized_companies` shows which exist.
- A suggestion — `classify_item`, or a `suggested` value from `explain_rejection` — goes on a
  document only after the user accepts it.
- `contingency` on `issue_invoice` is for a SEFAZ that is down, never a retry for a rejection.
- Webhook tools need `webhook:manage`, asked for on first use. Never repeat a webhook secret.
- Ask `get_company_readiness` once per change, never in a loop. Write the company's address
  with `update_company` only after the user confirms it; fiscal fields only as the user states
  them.
