---
name: cancel-invoice
description: Cancel an authorized fiscal document, or file a correction letter when cancelling is not what the situation needs.
---

# Cancelling, and what is not cancelling

Cancelling has fiscal and accounting effect and cannot be undone. The tax authority enforces
a window, and for an NFS-e it varies by municipality. Outside it, cancelling is refused, and
there is no other operation here that undoes the document.

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
| Values, taxes, recipient, service description | Cancel and issue again |
| The document was **rejected**, not authorized | `reissue_invoice` — there is nothing to cancel |
| The window has closed | Neither: say so plainly instead of retrying |

**Correcting a document is not available here.** The correction letter exists for NF-e, and
this connector serves NFS-e only — do not offer it, and do not claim a wording change can be
fixed after the fact.
