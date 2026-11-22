---
name: manage-items
description: Find, read, save and fix the company's catalog of products and services — the lines reused between issuances — without issuing anything.
---

# The company's catalog

A line typed into `issue_invoice` is retyped, and its NCM guessed again, every month. The
catalog keeps it once: `issue_invoice` takes its id as `item_id` on a line, and the
description, the price and the fiscal codes come from there. Nothing here issues a document or
spends a credit.

An item is a **product** (goods, NF-e) or a **service** (NFS-e). `kind` decides which fiscal
fields it may carry; a field of the other kind is refused.

## Finding one

`list_items` — `search` takes part of the description, the code or the external reference;
digits also match the NCM and the GTIN. `kind` narrows to products or services. Most recently
used first; `limit` defaults to 20 and stops at 100, and `offset` pages. `total` is how many
match, not how many came back, so **absence from one page is not absence from the catalog**.

`list_items` shows active items; with `inactive` set it shows the deactivated ones instead.
When an item the person knows exists does not show up, look there before saving it again,
and bring it back with `reactivate_item`. `deactivate_item` hides one that is no longer sold —
it is kept, it still holds its code, and issuing with its id is refused until it is
reactivated; confirm with the person first.

`get_item` with the id reads one item with its fiscal fields. Each record carries `source` —
`manual`, `import`, `nuvemshop` or `invoice` — and `last_used_at` and `uses_count`.

## Saving one

`save_item` with `kind` and `description` (at most 120 characters for a product, 2000 for a
service). The rest is optional: `code` (the SKU), `unit_price`, `unit`, `external_reference`,
`notes`, and the fiscal fields:

- **Product** — `ncm` (8 digits), `cfop`, `tax_situation` (an ICMS CST or a CSOSN), `origin`
  (needs `tax_situation`), `cest`, `gtin`.
- **Service** — `service_code` (LC 116, like `1.07`) and `iss_retained`.

**Nothing fiscal is required to save**, and an NF-e still refuses a line with no `ncm` and
`cfop` when it is issued. So a product may be saved before it is classified; classify it
first with `fiscal-lookup` when the person wants it ready to issue.

**Saving without an `item_id` is an upsert.** An item with the same `external_reference`, or
the same `code` when none is sent, is updated with the fields sent instead of duplicated, and
the same call twice never makes two items. A `code` that belongs to a *different* item is
refused with that item's id — read it with `get_item`, show it to the person, and update that
one instead.

## Fixing one

`save_item` with `item_id` updates that item, and **only the fields sent change**. The result
is checked as a whole: turning a product into a service while it still has an `ncm` is
refused. `source` never changes.

## Issuing from the catalog

On an `issue_invoice` line, `item_id` fills what the line leaves out — what the line sends
wins. See `issue-invoice`. Two refusals worth reading, not working around: a service on an NF-e
or a product on an NFS-e (`ITEM_KIND_MISMATCH`), and a tax situation that needs a base and a
rate the catalog does not keep (`ITEM_TAX_REQUIRED`), where the line has to send its own `tax`.

## What not to do

- Do not save an NCM, a CFOP or a tax situation you inferred. A `classify_item` suggestion is
  a suggestion: show it, and save it only after the person confirms it. The next invoice
  will trust it.
- Do not create a second item for one that is only deactivated, or only on another page.
- Do not save an item to work around a lookup: classification belongs to `fiscal-lookup`.
