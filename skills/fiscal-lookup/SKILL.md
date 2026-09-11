---
name: fiscal-lookup
description: Resolve an NCM, CFOP, CEST or other published fiscal code before it goes on a document, instead of guessing one.
---

# Looking a fiscal code up

Read-only. These read published tables — nothing here issues, changes or cancels a
document.

## Which classification answers which question

They are not interchangeable, and a code from the wrong family is simply wrong.

- **NCM** — what the *thing* is. Goods only, eight digits.
- **CFOP** — what the *operation* is: a sale, a return, a transfer, an industrialization.
- **CEST** — goods under tax substitution, and only those.
- **CST / CSOSN** — the tax situation. CST for the regime normal, CSOSN for Simples
  Nacional. Which applies is a property of the company, not of the item.
- **ISS service** — services, for an NFS-e.

`list_fiscal_kinds` answers what exists for a country today. Ask it rather than assuming
— the list grows, and `ibs_cbs_class` exists only because of the 2026 tax reform.

## Finding one

`search_fiscal_codes` when the person described a thing: *"what NCM is a keyboard"*.
Pass `kind` whenever the question already names one; leaving it out searches every
classification at once, which is the most expensive call here and returns noise from
families that were never relevant.

`lookup_fiscal_code` when they already have a code and want it confirmed.

**The person chooses the code, not you.** Read the matching descriptions back and let
them decide. These codes determine the tax owed, and a confident wrong one is worse than
a question: the authority authorizes it now and refuses it later, which costs a
cancellation and a reissue.

If nothing matches, say nothing matched. Do not offer the nearest row as though it were
the answer, and never fall back to a code you remember — that is the exact failure these
tools exist to prevent.

`metadata` carries whatever the family publishes beyond a code and a description, and it
differs: `utrib` on an NCM, `ncm_code` on a CEST, `tax_type` on a CST, nothing at all on
an ISS service. Report what is there instead of expecting a fixed shape.

## Where this fits

Before `issue_invoice`, not after. The point is to fill the document with a code that
resolves, so `validate_invoice_payload` and then the authority both accept it.

An NF-e needs `ncm` and `cfop` on every item — `issue-invoice` covers the rest of what it
requires. To confirm who the recipient is, see `taxpayer-lookup`.
