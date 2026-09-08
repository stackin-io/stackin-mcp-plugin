---
name: diagnose-invoice
description: Explain why a fiscal document was rejected and what has to change, using what the tax authority actually answered.
---

# Diagnosing a rejection

A rejected document has a reason, and it is not a guess: the tax authority returns a code and
a message.

## Order

1. `list_invoices` with `status: "rejected"` — find the document and take its **`id`**, not
   its access key. A rejected document has no access key.
2. `get_invoice_submissions` with that id. This is where the answer is. Each attempt carries
   `status`, `detail` (the authorizer's message, in its own words), `environment`
   (`homologation` or `production`), `http_status`, `created_at`, and `raw_request` /
   `raw_response` exactly as they went over the wire. The tax authority's own rejection code
   — `209`, `539` and so on — lives inside `detail` and `raw_response`; `http_status` is the
   HTTP code of the transmission and is not it.
3. Explain, then say what to change.

## Reading it

- **Quote the code and the message.** The code is what the person will search for, what a
  support ticket needs, and what their accountant recognises. Paraphrasing it destroys its
  only value.
- **Say which environment the attempt ran in.** A rejection in homologation cost nothing and
  blocked no real invoice; the same words in production mean a document the client never
  received.
- **The rows are attempts, not documents.** A reissued invoice has several, oldest first.
  Only the last describes the current state.
- **`raw_response` keeps the authority's own shape** and is deliberately not normalized.
  Read it; do not invent a tidier structure for it.

## Then

| The document is | Operation |
|---|---|
| Rejected | `reissue_invoice` with the id, after fixing the data — it spends a credit like a fresh issuance, so it takes an `idempotency_key` for the same reason |
| Authorized NF-e, wording wrong | `correct_invoice` — a CC-e, free, no number burned |
| Authorized NFS-e, wording wrong | Cancel and issue again — there is no correction letter for services |
| Authorized, values wrong | Cancel and issue again |

Before reissuing, `validate_invoice_payload` on the corrected data — it catches a malformed
NCM or CFOP without spending another attempt.

## What this cannot tell you

The submission carries what the authority said, not why the data was wrong in the first
place. A rejection for an invalid state registration means the registration is wrong
somewhere — in the company's registration or in the recipient's — and no tool here reads
either. Say so rather than guessing which.
