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

It pages: `limit` defaults to 20 and stops at 100, and `offset` walks back through the
history. **Absence from one page is not absence from the history** — say what you looked at,
rather than concluding a document does not exist because it was not on the first page.

Every row carries **two identifiers, and they are not interchangeable**:

- `access_key` — what `consult_invoice`, `cancel_invoice` and `get_invoice_pdf` take.
- `id` — what `reissue_invoice` and `get_invoice_submissions` take.

A rejected row has an `id` and **no access key**: the authorizer never assigned one. That is
not missing data.

## Reporting

**Neither `consult_invoice` nor `list_invoices` returns the environment.** They answer with
`id`, `access_key`, `status` and `protocol` — a homologation document and a real one look
identical there, and someone reading "authorized" without that context can believe they
invoiced a client when they did not.

The environment is fixed on the credential the connection uses, so it is the same for
everything this connection sees; `get_invoice_submissions` is the one tool that states it per
attempt. Say where the value came from, and never infer it from a status.

`get_invoice_pdf` returns the printable rendering for either type — a DANFE for an NF-e, a
DANFSe for an NFS-e — base64-encoded in `content_base64`. The XML is the legally valid
document; the PDF is a convenience. A `502` from it means the authorizer is unavailable, not
that the invoice is wrong: say which, because the two lead the person to do opposite things.
