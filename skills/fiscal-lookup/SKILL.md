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

## A suggestion from the description

`classify_item` takes what the item is, in the person's words, and the document type, and
suggests an NCM, CFOP, CST/CSOSN, CEST or service code. Pass `recipient_state` when it is
known: it decides an intrastate (5xxx) or interstate (6xxx) CFOP.

- **It is a suggestion, whatever the confidence.** Show the primary candidate, its
  `confidence` and the alternatives, and say it is a suggestion. A plausible wrong NCM is
  authorized by the SEFAZ today and caught at an audit later.
- Confirm the chosen code with `lookup_fiscal_code`, and put it on an item only after the
  person accepts it.
- When `missing_information` is not empty, ask the person exactly those questions and call
  again with the answers in the matching arguments (`operation_scope`, `purpose`,
  `contains_alcohol`, `service_city_code`, `tax_retained`). Do not answer them yourself.

`metadata` carries whatever the family publishes beyond a code and a description, and it
differs: `utrib` on an NCM, `ncm_code` on a CEST, `tax_type` on a CST, nothing at all on
an ISS service. Report what is there instead of expecting a fixed shape.

## Where this fits

Before `issue_invoice`, not after. The point is to fill the document with a code that
resolves, so `validate_invoice_payload` and then the authority both accept it.

An NF-e needs `ncm` and `cfop` on every item — `issue-invoice` covers the rest of what it
requires. To confirm who the recipient is, see `taxpayer-lookup`.
