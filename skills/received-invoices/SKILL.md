---
name: received-invoices
description: Read the NF-e documents other companies issued against this one, and file the company's position on them.
---

# Documents issued against this company

The mirror of the issuance history: `list_invoices` shows what the company issued,
`list_received_invoices` shows what was issued **against** it. NF-e only — a service invoice
has no distribution channel.

Before a manifestation the SEFAZ sends a summary only. The full document arrives after one.

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

1. `list_received_invoices` — find the document, read the issuer and the amount back.
2. Ask which position the person means. Offer the four in plain words, not codes.
3. `manifest_received_invoice`.

## What not to do

- Do not pick a code because the person sounds unsure. "I don't recognise this" in
  conversation is not the same as filing `210220` with the SEFAZ.
- Do not file `210240` without the reason the person gave you, in their words.
- Do not treat a manifestation as reversible. Once accepted, it stands.
