---
name: consult-invoice
description: Find a fiscal document and report its current state, by access key or by searching the company's history.
---

# Looking a document up

Read-only. Nothing here changes a document.

## When the person has the access key

`consult_invoice` with the key and the document type. It answers with the current status
straight from the tax authority.

## When they do not

`list_invoices` — filters by document type and status (`pending`, `authorized`,
`rejected`, `cancelled`), newest first. Use it for "my last invoices", "what was rejected
today", or to find the document being described.

Every row carries **two identifiers, and they are not interchangeable**:

- `access_key` — what `consult_invoice`, `cancel_invoice` and `get_invoice_pdf` take.
- `id` — what `reissue_invoice` and `get_invoice_submissions` take.

A rejected row has an `id` and **no access key**: the authorizer never assigned one. That is
not missing data.

## Reporting

Say which environment the document was issued in. A homologation document looks identical
and has no fiscal value — someone reading a status without that context can believe they
invoiced a client when they did not.

`get_invoice_pdf` returns the printable rendering for either type — a DANFE for an NF-e, a
DANFSe for an NFS-e. The XML is the legally valid document; the PDF is a convenience.
