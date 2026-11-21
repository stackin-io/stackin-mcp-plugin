---
name: issue-invoice
description: Issue a Brazilian fiscal document — an NF-e for goods or an NFS-e for services — checking the data before it reaches the tax authority.
---

# Issuing a fiscal document

A document issued in **production** is legally binding and consumes a credit. One issued in
**homologation** is a test with no fiscal value and costs nothing — the environment is fixed
on the credential, not chosen per call, so check which one the connection is on before
telling anyone their invoice is real. Confirm the data with the person whenever you inferred
any field.

## Which document

- **NF-e** — goods. Needs, per item, an **NCM** and a **CFOP** (4 digits starting with 1, 2,
  3, 5, 6 or 7), and the recipient's full address including the **IBGE city code**. The NCM
  is 8 digits; a 2-digit chapter is accepted where the classification really is at that
  level, and is not a shortcut for not knowing the rest.
- **NFS-e** — services. Needs none of that: description, price, the client's name and their
  taxpayer ID are enough, and the recipient's address is optional. Each item also carries a
  **service_code** (LC 116/2003 `item.subitem`); leaving it out falls back to the company's
  fiscal profile, so send it only when this service differs from what that profile issues.
  Two more are NFS-e only: `service_discount` for an unconditional discount, and
  `tax_retained` when the ISSQN is withheld by the buyer.

Asking which one is cheaper than issuing the wrong one. A service invoiced as NF-e is not a
formatting mistake, it is the wrong fiscal document.

## The recipient

Look the recipient up with **`list_clients`** before typing one. It searches the company's
saved clients by part of the name or by CPF/CNPJ, most recently used first. When the client
is there, pass its id as **`client_id`**: the registry fills the name, the document and the
address, and `client_name` and `tax_id` become optional. A recipient retyped every month is
typed differently every month; the saved one is the same each time.

- **One match** — read the name and the document back, then use its id.
- **Several** — ask which one. Two clients with similar names are two different taxpayers.
- **None** — send `client_name` and `tax_id` as before. A new recipient is saved as a client
  after a successful issuance, so the next invoice finds it.

Anything sent alongside `client_id` overrides the saved data for this document only. Set
**`update_client: true`** when the person says the client itself changed — a new address, a
new email — so the registry keeps the correction. Do not set it for a one-off difference.

`list_clients` shows active clients only; a client that is not found may be deactivated —
`list_clients` with `inactive` set shows those, and `reactivate_client` brings one back. Saving or fixing a client without issuing anything is the
`manage-clients` skill.

## What a line is worth

Each item takes **`unit_price`** — the price of one unit — or **`amount`** — the line's gross
total, before discount and freight. `quantity` defaults to 1, so for a single unit the two are
the same number.

Send whichever the person actually said. "R$ 120 each, two of them" is
`quantity: 2, unit_price: 120`; "R$ 240 the line" is `amount: 240`. Sending both asserts they
agree, and a mismatch is refused with `ITEM_TOTAL_MISMATCH` naming the line and both numbers —
that refusal is the point, so do not "fix" it by dropping one of the two.

Never multiply or divide to fill the other field. A rounded third of a price is a different
document from the one the person described.

## Before a company's first document

`get_company_readiness` answers whether the company can issue right now. When `ready` is
false, `missing` names the cause — `certificate`, `certificate_expired`,
`certificate_unreadable`, `address`, `state_registration`, `plan` — and `by_document_type`
names the fields at fault per document type. Do not issue anyway: that only spends an attempt
on a refusal. An `address` or `state_registration` is completed here with `update_company`,
after the person confirms it; the rest only in the dashboard, at `fix_url`. The whole path —
readiness, completing the company, a test in homologation, then production — is the
`first-invoice` skill.

Ask it once, and again only when something changed or issuing fails for a reason that is not
the document's — never in a loop. It also gives the certificate's expiry, the tax regime
(CRT), the state and the default série per document type.

## The city

Issuing resolves the IBGE `city_code` from the city and state by itself. Use `search_cities`
only when a name matches more than one municipality, or when the API answered
`CITY_NOT_FOUND`: it returns up to 20 with code, name and state. When more than one fits, ask
which — never pick the first.

## Optional fields, only when asked

- **`discount`** — a discount on the whole document, in BRL. The API spreads it over the
  lines in proportion to each line's amount; a per-line discount goes on the item instead.
- **`issued_at`** — the emission date-time, ISO 8601 **with a timezone offset**
  (`2026-11-15T09:30:00-03:00`); without one it is refused. Omitted means now. Send it only
  when the person asks for another date: an NF-e takes at most 30 days back and 5 minutes
  ahead, an NFS-e never a future one.
- **`contingency`** — NF-e only. Sends through the state's contingency authorizer
  (SVC-AN or SVC-RS) because the state SEFAZ itself is down. Only when the person says the
  SEFAZ is unavailable — **never as a retry for a rejection**: a rejection is about the data,
  and contingency does not change the data.

## Order

1. `list_clients` — find the recipient, and take its id when it is saved.
2. `validate_invoice_payload` — checks NCM, CFOP, amounts and the address without sending
   anything. Nothing is issued, so it is safe while the data is still being assembled.
3. Fix what it reports.
4. `issue_invoice`, with `client_id` when step 1 found the client.
5. Report the outcome: the status, the access key, and — when the authorizer refused — its
   own message.

When the connection covers several companies, every one of these calls also names the
issuing company with `company_id` or `company_tax_id` — see `select-company`.

## What not to do

- Do not invent an NCM or a CFOP. A wrong one is a rejection, and the person who asked has
  no way to know it was guessed.
- Do not invent an address. Ask — or take it from the saved client.
- Do not retype a recipient the registry already has. The saved name and address are the
  ones earlier documents went out with; a retyped one drifts from them.
- Do not retry a failed issuance blindly. A lost response does not mean nothing was issued —
  pass an **`idempotency_key`** on the first call and reuse it on the retry, which replays the
  first answer instead of issuing a second document. Without one, check `list_invoices` before
  trying again. One key per business event, never one per call: two invoices for the same
  customer and amount on the same day are a normal thing to issue, and a per-call key would
  protect nothing.
- Do not pass `series` or `number` unless the person gave them. The company's numbering
  answers for itself, and a hand-picked number collides with it.
