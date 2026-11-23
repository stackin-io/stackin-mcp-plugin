---
name: received-invoices
description: Read the NF-e documents other companies issued against this one, and file the company's position on them.
---

# Documents issued against this company

The mirror of the issuance history: `list_invoices` shows what the company issued,
`list_received_invoices` shows what was issued **against** it. NF-e only — a service invoice
has no distribution channel.

Before a manifestation the SEFAZ sends a **summary** only (`resNFe`): access key, issuer,
amount, date. The **full document** (`nfeProc`) arrives after one; `has_full_document` says
whether it is already stored. Reading the list never calls the SEFAZ. Collection runs on a
schedule, every six hours, and `sync_received_invoices` asks now. After a read that finds
nothing more the SEFAZ makes the CNPJ wait **one hour** — inside that wait the sync answers
that it is too soon and says when to try; do not retry in a loop.

**Cost.** Every plan includes **50 received NF-e a month**; past that, each new one costs
**R$ 0,05**, taken from the account's credit. Some older accounts are exempt.
`get_usage` shows `used_received`, `included_received`, `received_price_cents` and
`received_free` — read it before telling someone a sync is free.

The list pages the same way `list_invoices` does, with `limit` and `offset`.

## Downloading the full XML

`get_received_invoice_xml` with the access key returns the stored `procNFe`. Downloading is
not charged — a received document is billed once, when it is stored. Until the full document
has arrived it answers that only the summary is there: the SEFAZ sends the full XML only after
a manifestation (`210210` or `210200`), on a later read (the scheduled one, or
`sync_received_invoices`). Offer that path; never file a manifestation just to get the XML
without the person choosing the position.

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
   row carries `access_key`, `issuer_name`, `issuer_tax_id`, `amount`, `issued_at`,
   `manifestation` and `final_answer_due`. **Check the manifestation first**: a row that
   already carries a position was already answered, and filing again is a second
   declaration, not a correction. `final_answer_due` set means only an awareness (`210210`)
   was filed and a conclusive answer is still owed.
2. Ask which position the person means. Offer the four in plain words, not codes.
3. `manifest_received_invoice`.

## What not to do

- Do not pick a code because the person sounds unsure. "I don't recognise this" in
  conversation is not the same as filing `210220` with the SEFAZ.
- Do not file `210240` without the reason the person gave you, in their words. It is the only
  one that takes a reason, and the other three are **refused** if one is sent.
- Do not treat a manifestation as reversible. Once accepted, it stands.
