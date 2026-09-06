---
name: cancel-invoice
description: Cancel an authorized fiscal document, or file a correction letter when cancelling is not what the situation needs.
---

# Cancelling, and what is not cancelling

Cancelling has fiscal and accounting effect and cannot be undone. The tax authority enforces
a window: **24 hours for an NF-e**, and it varies by municipality for an NFS-e. Outside it,
cancelling is refused and the fix is a different operation.

## Confirm before, always

1. `consult_invoice` — read the client, the amount and the date **back to the person**.
   "Cancel the last one" is not an identification; a wrong cancellation is a fiscal event,
   not a mistake to undo.
2. Confirm the reason. It reaches the tax authority verbatim and must be at least
   15 characters.
3. `cancel_invoice`.

## When cancelling is the wrong tool

| Situation | Operation |
|---|---|
| Wording, carrier, extra information | `correct_invoice` — a correction letter (CC-e) |
| Values, taxes, recipient, products | Cancel and issue again — a CC-e cannot touch these |
| The document was **rejected**, not authorized | `reissue_invoice` — there is nothing to cancel |

A correction letter does not consume a credit and does not burn a number in the series. Each
one supersedes the previous, and the authority keeps at most 20 per document.

## Documents issued against the company

`list_received_invoices` lists what other companies issued **against** this one — the mirror
of `list_invoices`. It reads what was already collected and never calls the tax authority,
which caps how often a company may ask per day.

`manifest_received_invoice` is also irreversible: it is a declaration to the tax authority,
not a note to self. Four codes — 210200 confirms the operation, 210210 acknowledges the
document, 210220 denies knowing it, 210240 states the operation was not carried out. **Only
210240 takes a reason, and it requires one.**
