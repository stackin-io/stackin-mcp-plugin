---
name: fiscal-lookup
description: Resolve an NCM, CFOP, CEST or other published fiscal code before it goes on a document, instead of guessing one, and simulate the IBS/CBS of a set of lines.
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
  person accepts it. A code the person will reuse is kept with `save_item`; see
  `manage-items`.
- When `missing_information` is not empty, ask the person exactly those questions and call
  again with the answers in the matching arguments (`operation_scope`, `origin`, `purpose`,
  `contains_alcohol`, `service_city_code`, `tax_retained`). Do not answer them yourself.
- **`origin`** says whether the company resells the goods (`resale`, CFOP `x102`) or sells its
  own production (`own_production`, `x101`). The same item gets a different CFOP for each, so
  when the question comes up, ask the person; never assume one.

`metadata` carries whatever the family publishes beyond a code and a description, and it
differs: `utrib` on an NCM, `ncm_code` on a CEST, `tax_type` on a CST, nothing at all on
an ISS service. Report what is there instead of expecting a fixed shape.

## The NBS of a service

`suggest_nbs` takes an NFS-e service code (`1.07`, `01.07.00` or `010700`) and lists the NBS
codes Anexo VIII pairs with it, each with the `operation_indicator` (cIndOp) and
`ibs_cbs_classification` (cClassTrib) the annex lists. Each row also carries, when the
official tables give them, `classification_cst` (the CST for the item's `ibs_cbs`),
`reduction_ibs` and `reduction_cbs` (the cClassTrib's reduction, in percent), `legal_reference`
(the LC 214/2025 article behind it), `incidence` (where the annex says the IBS is due) and
`operation_variants` (the cIndOp for the same operation when it is not onerous or the acquirer
is abroad: `onerous_domestic`, `onerous_abroad`, `free_domestic`, `free_abroad`). Show the
legal basis and the reductions with the row, so the person picks knowing what each one means.
They are suggestions: show them, let the person pick one, and only then put it on the item as
`nbs`, with the other fields in the item's `ibs_cbs` group when the person also confirms them.
An empty list means the annex lists none for that code, not that the code is wrong.

## Simulating IBS/CBS

`calculate_ibs_cbs` shows what the IBS and CBS would come to for a set of lines, before any
document exists. It is read-only, needs the `invoice:read` scope and takes no `company_id`.
It issues nothing and the answer is not a fiscal document: always `simulated: true`, and say
so to the person.

Send:

- **`items`** — one to 990 lines, each with `cst` (3 digits) and `classification` (the
  cClassTrib, 6 digits), plus `amount` (the item's amount, used as the base when no `base` is
  given) or `base` (the vBC). `reduction_ibs` and `reduction_cbs` (pRedAliq, in %) only when
  the person gave them.
- **`operation_date`** — `YYYY-MM-DD`, required. It picks the vigência and the rates.
- **`document_type`** — `nfe` (the default), `nfce` or `nfse`: the model the cClassTrib is
  checked for.
- **`rate_state`**, **`rate_city`**, **`rate_federal`** (pIBSUF, pIBSMun, pCBS, in %) — only
  when the person gave them.

Rates left out use the official 2026 ones: CBS 0.9%, IBS UF 0.1%, IBS Mun 0%. Outside 2026
they are required, and leaving them out is a 422 `IBS_CBS_RATES_REQUIRED` — ask the person for
the rates, do not carry the 2026 ones to another year.

The answer has the amounts per item and in total (`vBC`, `vIBSUF`, `vIBSMun`, `vIBS`, `vCBS`,
`vDif`), the indicators, and whether the `gIBSCBS` group would be written. Report them as
they come.

- **For an NFS-e the values are the NF-e engine's.** The Sefin Nacional computes the real
  ones, so tell the person the figures are an estimate, not what the authority will return.
- **The refusals are the issuance's.** The same 422 codes, among them
  `IBS_CBS_CLASS_CST_MISMATCH` (the classification does not go with that CST) and
  `IBS_CBS_CLASS_NOT_IN_FORCE` (not in force on `operation_date`). Fix the pair with
  `lookup_fiscal_code` on the `ibs_cbs_class` kind and let the person choose; never swap in
  another classification to make it pass.

## Where this fits

Before `issue_invoice`, not after. The point is to fill the document with a code that
resolves, so `validate_invoice_payload` and then the authority both accept it. To see the
IBS/CBS a set of lines would carry first, simulate it with `calculate_ibs_cbs`.

An NF-e needs `ncm` and `cfop` on every item — `issue-invoice` covers the rest of what it
requires. To confirm who the recipient is, see `taxpayer-lookup`.
