---
name: cancel-invoice
description: Cancel an authorized fiscal document, or file a correction letter when cancelling is not what the situation needs.
---

# Cancelling, and what is not cancelling

Cancelling in production has fiscal and accounting effect and cannot be undone. In
homologation it is a test like any other. The tax authority enforces
a window, and for an NFS-e it varies by municipality. Outside it, cancelling is refused, and
there is no other operation here that undoes the document.

## Confirm before, always

1. `consult_invoice` — read the client, the amount and the date **back to the person**.
   "Cancel the last one" is not an identification; a wrong cancellation is a fiscal event,
   not a mistake to undo.
2. Confirm the reason. It reaches the tax authority verbatim and is 15 to 256 characters.
3. `cancel_invoice`. If the call has to be retried — a timeout, a lost answer — repeat it
   with the same **`idempotency_key`**, which replays the first response instead of
   cancelling twice. Two calls without a key are two cancellations.

## When cancelling is the wrong tool

| Situation | Operation |
|---|---|
| Values, taxes, recipient, service description | Cancel and issue again |
| The document was **rejected**, not authorized | `reissue_invoice` — there is nothing to cancel |
| The window has closed | Neither: say so plainly instead of retrying |

**Try a correction letter before cancelling an NF-e.** A CC-e (`correct_invoice`) fixes
wording — a product name, transport details, extra information — for free: no new credit, no
burned number. It cannot touch anything that changes the tax owed, the parties or the issue
date, and it does not exist for NFS-e, where the answer really is cancel and issue again.

The cancellation window differs by document, and neither is ours to set: for an NFS-e the
municipality defines it, and for an NF-e the SEFAZ's general rule is 24 hours from
authorization, with some states accepting a late cancellation under penalty. The authorizer
decides — so do not promise a window, and do not read a refusal as a bug. Outside it, the
answer is a reversing document, which is an accountant's call rather than this connector's.
