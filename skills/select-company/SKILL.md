---
name: select-company
description: Pick which company a call acts for when one connection covers several, and read what each one allows.
---

# Choosing the company

One connection authorized through the consent screen may cover several companies, each with
its own permissions. A connection that covers a single company needs none of this: leave the
company out and that company is used.

## Seeing them

`list_authorized_companies` answers from the connection itself. Each row carries:

- `company_id` — the UUID, accepted as `company_id`;
- `tax_id` — the company's CNPJ or CPF, accepted as `company_tax_id`;
- `name`;
- `permissions` — `invoice:read` consults and lists, `invoice:issue` issues and reissues,
  `invoice:write` corrects and manifests, `invoice:cancel` cancels and invalidates
  numbering, `company:write` completes the company's own address and fiscal fields
  (`update_company`), `webhook:manage` lists, creates and deletes webhooks and reads their
  deliveries. `webhook:manage` is granted on demand, not at connect: the client asks the
  person to authorize again the first time a webhook tool is used, so its absence from the
  list is not a refusal.

The listing also says the `environment` — `homologation` or `production` — and it is the
same for every company in it.

Call it before acting when the person has more than one company, or when a tool answered that
it needs one. Do not ask the person for a UUID; this is where it comes from.

## Naming the company on a call

Every tool that touches a company's documents takes `company_id` or `company_tax_id`.
**One of them, never both** — they name the same company two ways, and both at once is
refused before anything is sent. The lookups — `lookup_fiscal_code`, `search_fiscal_codes`,
`list_fiscal_kinds`, `search_cities` and `lookup_taxpayer` — read published tables, not a company's data, and
take neither.

`company_tax_id` is **the company using Stackin**, never the recipient and never a taxpayer
being looked up. `issue_invoice`, `save_client` and `lookup_taxpayer` each take a `tax_id` of
their own; filling the wrong one invoices or saves under the wrong company.

## Order

1. `list_authorized_companies`.
2. When there are several, ask which company this is for, by name — and check that its
   `permissions` allow what the person wants before calling the tool that does it.
3. Pass the same `company_id` or `company_tax_id` on every call of the task. Clients,
   invoices and received documents belong to one company; an id read under one company means
   nothing under another.

## What not to do

- Do not pick a company because it is first in the list.
- Do not switch companies mid-task without saying so.
- Do not read a refusal for a missing permission as a fault in the tool. The connection was
  granted less on that company; the person widens it by authorizing again.
