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
2. `get_invoice_submissions` with that id. This is where the answer is: `status_code` (the
   authority's own code — `209`, `539`, and so on), `detail` (its message), `endpoint`,
   `environment`, and the request and response exactly as they went over the wire.
3. Explain, then say what to change.

## Reading it

- **Quote the code and the message.** The code is what the person will search for, what a
  support ticket needs, and what their accountant recognises. Paraphrasing it destroys its
  only value.
- **The rows are attempts, not documents.** A reissued invoice has several, oldest first.
  Only the last describes the current state.
- **`raw_response` keeps the authority's own shape** and is deliberately not normalized.
  Read it; do not invent a tidier structure for it.

## Then

| The document is | Operation |
|---|---|
| Rejected | `reissue_invoice` with the id, after fixing the data |
| Authorized, wording wrong | `correct_invoice` |
| Authorized, values wrong | Cancel and issue again |

Before reissuing, `validate_invoice_payload` on the corrected data — it catches a malformed
NCM or CFOP without spending another attempt.

## What this cannot tell you

The submission carries what the authority said, not why the data was wrong in the first
place. A rejection for an invalid state registration means the registration is wrong
somewhere — in the company's registration or in the recipient's — and no tool here reads
either. Say so rather than guessing which.
