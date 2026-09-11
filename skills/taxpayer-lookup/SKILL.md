---
name: taxpayer-lookup
description: Confirm who a tax id belongs to before invoicing them, by exact match against the taxpayer registry.
---

# Checking who a tax id belongs to

Read-only. One tool, `lookup_taxpayer`, and one question: *who is this CNPJ I am about
to invoice*.

## This needs an API key, not OAuth

**`lookup_taxpayer` is refused over OAuth.** A connection made through the consent screen
answers `403` on every call, and **reconnecting does not fix it** — the server maps this
route to no scope, so there is no permission to grant. It works when the connection
carries the company's own API key.

## Exact match, and nothing else

Pass the id exactly. Punctuation is fine — `00.000.000/0001-91` works.

**There is no search by name, by prefix or by state, and there will not be.** This
registry holds the names and addresses of real people and companies. An exact lookup
answers the issuer's question; anything broader is a bulk export of personal data wearing
the costume of a query.

If the person does not have the id, they have to get it from the customer. Do not offer
to look for it, and do not try adjacent ids.

## A 404 is not proof the company does not exist

This is the rule that matters most here, because the obvious reading of a 404 is wrong.

The registry reloads **monthly**, from the Receita Federal's published dump. A company
registered in the last few weeks is genuinely absent from it and perfectly valid.

So when it answers 404:

- Say the registry has no record **yet**, not that the id is invalid.
- Do not block issuing. A real customer with a two-week-old CNPJ would be refused by
  that.
- Never turn it into a validation rule, in a prompt or anywhere else.

The tax authority validates the recipient at issuing time. That is the check that counts;
this one is a convenience for confirming a name.

## Reading the answer

`country`, `tax_id`, `kind` and `name` are always there. Everything else —
`trade_name`, `status`, `started_at`, `activity_code`, `state`, `city_code`,
`postal_code` — can be absent, because the registry publishes what it has. Report what
came back rather than treating a missing field as an error.

`status` is the registry's own code for the taxpayer's situation. If the person needs to
act on it, say what the field contains rather than interpreting it as active or inactive.

## Where this fits

Before issuing, to confirm the recipient's name matches who the person thinks they are
billing. The codes that go on the document itself are a different job — see
`fiscal-lookup`.
