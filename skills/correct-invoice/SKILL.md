---
name: correct-invoice
description: File a correction letter (CC-e) against an authorized NF-e — and know when a correction is not what the situation needs.
---

# Correcting an authorized NF-e

A CC-e is a public statement filed with the SEFAZ. It supersedes the previous letter, and the
authority keeps at most 20 per document.

## What a CC-e can and cannot do

| Wrong | Fix |
|---|---|
| Wording, additional information, non-fiscal fields | `correct_invoice` |
| Value, taxes, quantity, the products | Cancel and issue again — a CC-e leaves the wrong figures standing |
| The recipient | Cancel and issue again |
| An **NFS-e**, anything | Cancel and issue again — there is no correction letter for services |

Saying "I filed a correction" when the amount was wrong is worse than saying nothing: the
person believes the document is fixed, and the audit finds the original figures.

## Order

1. `consult_invoice` — confirm which document, and read the client, the amount and the date
   back to the person.
2. Read the correction text back too. It reaches the tax authority verbatim and is 15 to
   1000 characters.
3. `correct_invoice`.

## What not to do

- Do not offer a CC-e for a wrong value. Say plainly that it cannot fix that.
- Do not file one against a rejected document. There is nothing to correct — it was never
  authorized. Use `reissue_invoice` after fixing the data.
- Do not file a second letter to "add" to the first. Each one replaces the last, so the new
  text has to carry everything that still applies.
