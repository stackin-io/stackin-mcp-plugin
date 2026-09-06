---
name: issue-invoice
description: Issue a Brazilian fiscal document — an NF-e for goods or an NFS-e for services — checking the data before it reaches the tax authority.
---

# Issuing a fiscal document

An issued document is legally binding and consumes a credit. Confirm the data with the
person before issuing whenever you inferred any field.

## Which document

- **NF-e** — goods. Needs, per item, an **NCM** (8 digits) and a **CFOP** (4 digits starting
  with 1, 2, 3, 5, 6 or 7), and the recipient's full address including the **IBGE city
  code**.
- **NFS-e** — services. Needs none of that: description, amount, the client's name and their
  taxpayer ID are enough.

Asking which one is cheaper than issuing the wrong one. A service invoiced as NF-e is not a
formatting mistake, it is the wrong fiscal document.

## Order

1. `validate_invoice_payload` — checks NCM, CFOP, amounts and the address without sending
   anything. Nothing is issued, so it is safe while the data is still being assembled.
2. Fix what it reports.
3. `issue_invoice`.
4. Report the outcome: the status, the access key, and — when the authorizer refused — its
   own message.

## What not to do

- Do not invent an NCM or a CFOP. A wrong one is a rejection, and the person who asked has
  no way to know it was guessed.
- Do not invent an address. Ask.
- Do not retry a failed issuance blindly. If the response was lost the document may already
  exist; use `list_invoices` to see before issuing again.
