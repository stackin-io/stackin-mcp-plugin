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

## Order

1. `validate_invoice_payload` — checks NCM, CFOP, amounts and the address without sending
   anything. Nothing is issued, so it is safe while the data is still being assembled.
2. Fix what it reports.
3. `issue_invoice`.
4. Report the outcome: the status, the access key, and — when the authorizer refused — its
   own message.

## What not to do

- Do not invent an NCM or a CFOP. A wrong one is a rejection, and the person who asked has
  no way to know it was guessed.
- Do not invent an address. Ask.
- Do not retry a failed issuance blindly. A lost response does not mean nothing was issued —
  pass an **`idempotency_key`** on the first call and reuse it on the retry, which replays the
  first answer instead of issuing a second document. Without one, check `list_invoices` before
  trying again. One key per business event, never one per call: two invoices for the same
  customer and amount on the same day are a normal thing to issue, and a per-call key would
  protect nothing.
- Do not pass `series` or `number` unless the person gave them. The company's numbering
  answers for itself, and a hand-picked number collides with it.
