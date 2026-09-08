---
name: received-invoices
description: Read the NF-e documents other companies issued against this one, and file the company's position on them.
---

# Documents issued against this company

The mirror of the issuance history: `list_invoices` shows what the company issued,
`list_received_invoices` shows what was issued **against** it. NF-e only — a service invoice
has no distribution channel.

Before a manifestation the SEFAZ sends a **summary** only (`resNFe`): access key, issuer,
amount, date. The **full document** (`nfeProc`) arrives after one. Reading the list never
calls the SEFAZ — the
authorizer caps how often a CNPJ may ask for its distribution per day, so collection runs on a
schedule and asking again cannot spend that allowance faster.

The list pages the same way `list_invoices` does, with `limit` and `offset`.

## The four positions, and what each one claims

| Code | Meaning | Weight |
|---|---|---|
| `210200` | Confirms the operation happened | Routine |
| `210210` | Acknowledges the document exists, without confirming | Routine |
| `210220` | Denies knowing the document | **Accuses the issuer** |
| `210240` | States the operation was not carried out | **Accuses the issuer**, requires a reason |

The last two are not stronger versions of the first two. They tell the tax authority that a
document naming this company's CNPJ is wrong, which starts a problem for whoever issued it.

## Order

1. `list_received_invoices` — find the document, read the issuer and the amount back. Each
   row carries `access_key`, `issuer_name`, `issuer_tax_id`, `amount`, `issued_at` and
   `manifestation`. **Check that last one first**: a row that already carries a position was
   already answered, and filing again is a second declaration, not a correction.
2. Ask which position the person means. Offer the four in plain words, not codes.
3. `manifest_received_invoice`.

## What not to do

- Do not pick a code because the person sounds unsure. "I don't recognise this" in
  conversation is not the same as filing `210220` with the SEFAZ.
- Do not file `210240` without the reason the person gave you, in their words. It is the only
  one that takes a reason, and the other three are **refused** if one is sent.
- Do not treat a manifestation as reversible. Once accepted, it stands.
