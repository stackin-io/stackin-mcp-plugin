---
name: manage-clients
description: Find, read, save and fix the company's saved clients — the recipients reused between issuances — without issuing anything.
---

# The company's clients

A recipient typed into `issue_invoice` is retyped, and typed differently, every month. The
registry keeps it once: `issue_invoice` takes its id as `client_id`, and the name, the
document and the address come from there. Nothing here issues a document or spends a credit.

## Finding one

`list_clients` — `search` takes part of the name, or the CPF/CNPJ with or without
punctuation. `source` narrows to where the client came from (`manual`, `issued`, `issuance`
or `import`). Most recently used first unless `sort_by` (`name`, `last_used_at`, `created_at`
or `uses_count`) and `order_by` (`asc` or `desc`) say otherwise; `limit` defaults to 20 and stops at 100, and `offset`
pages. `total` is how many match, not how many came back, so **absence from one page is not
absence from the registry**.

`list_clients` shows active clients; with `inactive` set it shows the deactivated ones
instead. When a client the person knows exists does not show up, look there before saving
it again, and bring it back with `reactivate_client`. `deactivate_client` hides one that is
no longer used — it is kept, and the documents already issued to it still name it; confirm
with the person first.

`get_client` with the id reads one client with its full address. Each record carries
`source` — `manual` (saved by hand), `issued` (imported from issued invoices) or `issuance`
(saved by an issuance) — and `last_used_at` and `uses_count`.

## Saving one

`save_client` with `name` and `tax_id`. The CPF/CNPJ is required except for a buyer abroad,
whose address carries `state: "EX"` and whose document goes in `foreign_id`. The rest is
optional: `state_registration`, `municipal_registration` (up to 15 characters),
`email`, `phone`, `address` and `notes` (up to 500
characters).

There is usually no need to: a new recipient is saved after a successful issuance on its
own. Save by hand when the person wants the client ready before the first invoice, or wants
to keep data the invoice does not carry, like an email or notes.

**A document that is already saved is refused**, and the refusal carries the existing
client's id. That is not an error to work around: read it with `get_client`, show it to the
person, and update that one instead of creating a second.

## Fixing one

`save_client` with `client_id` updates that client, and **only the fields sent change** —
leave out what the person did not mention. `name` is always sent, so send the saved name
back when only something else changed.

Correcting a client while issuing is `issue_invoice` with `update_client: true` instead; see
`issue-invoice`.

## What not to do

- Do not save data you inferred. Read it back and let the person confirm it — the next
  invoice will trust it.
- Do not save a client to work around a lookup. A tax id the person is unsure of is a job for
  `taxpayer-lookup` first.
- Do not create a second record for a client that is only deactivated, or only on another
  page.
