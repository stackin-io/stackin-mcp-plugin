---
name: manage-webhooks
description: Register, list and remove the URLs that receive a company's document events, and check whether one is actually receiving.
---

# Managing webhooks

A webhook sends every authorized, rejected, cancelled and corrected document — with its
data — to a URL. Pointing one somewhere is not a read and not an issuance either, so every
tool here needs **`webhook:manage`**, a scope of its own. It is granted on demand, not at
connect: the first time one of these tools is used, the client asks the person to authorize
again. That prompt is expected, not an error.

An endpoint receives the events of the connection's environment only — a homologation
connection never delivers production documents, and the other way round.

## Before creating one

`list_webhooks` first. Each row is one endpoint: its `id` (what `delete_webhook` takes), the
URL, the events and whether it is active. Secrets are never returned.

**Every endpoint gets every event it subscribes to.** Two registrations of the same URL are
two endpoints, and the integration receives each document twice. If the URL is already
there, say so instead of registering it again.

## Creating one

`create_webhook` only with:

- **an `https://` URL the person gave** — never one you composed. Read it back and confirm
  it before calling: it is where their fiscal data goes. The API refuses a URL that is not
  HTTPS or points at a private network.
- **a secret the person chose**, 16 to 255 characters; every delivery is signed with it.
  Do not generate one for them, and **never repeat it back** — not in the confirmation, not
  in the summary. It is not shown again by any tool.
- `events` only when the person wants fewer than all four (`invoice.authorized`,
  `invoice.rejected`, `invoice.cancelled`, `invoice.corrected`); omitted means every one.

## Removing one

`delete_webhook` with the endpoint's id from `list_webhooks`. Delivery stops from that
moment: the integration no longer hears about new documents. Confirm **which** endpoint by
its URL first, when there is more than one. What was already delivered stays in the
deliveries.

## "Is my webhook receiving?"

`list_webhook_deliveries`, newest first. Each row has the event, its status, how many
attempts, what the endpoint answered (`response_status`), the `last_error` and when it was
delivered or will be retried. Read those back:

- a `response_status` of 2xx is a delivery the endpoint accepted;
- any other status, or a `last_error`, is the endpoint's side refusing or failing — quote
  it, because that is what the person's developer needs;
- no rows at all means no event has happened since the endpoint was registered, not that
  delivery is broken.

When the connection covers several companies, every call names the company with
`company_id` or `company_tax_id` — see `select-company`.
