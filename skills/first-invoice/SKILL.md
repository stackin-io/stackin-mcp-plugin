---
name: first-invoice
description: Take a new company from "not ready" to its first real document — readiness, completing the company here, a test in homologation, then production.
---

# The first invoice

A company that just connected usually cannot issue yet, and the reason is almost always one
field away. This is the order that gets it there without sending the person to a dashboard —
and without asking the same question twice.

## 1. Ask once what is missing

`get_company_readiness`. When `ready` is true, go straight to step 3. When it is false,
`missing` names the cause and `by_document_type` breaks it down per `nfe` and `nfse`: each
blocker carries a `code` and, for the address, the `fields` at fault; each warning names a
default being declared (`tax_regime_default`, `simples_nacional_default`,
`service_code_default`). `fix_url` is the dashboard screen for the first blocker.

A company ready for one document type and not the other is ready: say which one it can issue.

**Do not call it again until something changed** — an `update_company`, or the person saying
they fixed something. The answer will be the same, and asking it in a loop is how a person
gives up before their first invoice.

## 2. Complete the company

What blocks decides who fixes it.

- **`address`** — fixed here.
  1. `lookup_taxpayer` with the company's own CNPJ (the `tax_id` readiness answered). The
     registry holds the address the company registered: `street_type` + `street`, `number`
     and `neighborhood` under `metadata.address`, the CEP as `postal_code`.
  2. The city needs one more hop. The row's `city_code` is the Receita's code (4 digits,
     e.g. `7107` for São Paulo), **not** the IBGE code, and the row has no city name. Get the
     name with `lookup_fiscal_code(kind="city", code=<city_code>)`. Never copy or pad
     `city_code` into `municipality_code`.
  3. Show the person that address — street, number, neighborhood, city and CEP — and ask
     whether it is where the company issues from.
  4. Only after they confirm, `update_company` with those fields, the city as
     `municipality_name`: the IBGE code is found from it in the company's state. Sending
     `municipality_code` instead is fine only with the 7-digit IBGE code from
     `search_cities`. Leave out what neither the registry nor the person gave — never
     invent a field.
- **`state_registration`** (NF-e) — ask the person for the IE (digits, or `ISENTO`), then
  `update_company` with `state_registration`. Never take it from anywhere else.
- **`certificate`, `certificate_expired`, `certificate_unreadable`, `plan`** — only the
  dashboard fixes these. Give the person `fix_url` and stop until they say it is done.

The fiscal fields — `tax_regime`, `simples_nacional`, `state_registration`, `service_code` —
decide what every future document declares and owes. Send them only when the person states
them. A warning that a default is being declared, or a `suggested_fiscal_fields` value from
the registry, is something to **ask** about, never to write on your own; only the company's
owner may change them.

`update_company` answers with the readiness fields themselves. When `ready` is now true,
there is no need to ask `get_company_readiness` again.

### When `update_company` is refused

A connection made before company settings existed does not have `company:write`. The refusal
says so: tell the person to **reconnect Stackin to allow company settings** — approve it when
the client asks for it, or disconnect the `stackin` connector, connect again and approve
company settings on the consent screen — and,
if they would rather not, give them `fix_url` to fill the address in the dashboard. Retrying
does not help, and neither does another readiness call; wait for them to say they did one of
the two.

## 3. A test in homologation

Every connection is authorized for one environment, chosen on the consent screen;
`list_authorized_companies` says which. **Homologation** is a test with no fiscal value and
costs nothing — the right place for the first document.

Issue one following `issue-invoice`: `validate_invoice_payload`, then `issue_invoice`. An
authorized test proves the certificate, the address and the numbering together. A rejection
here is cheap: read it with `diagnose-invoice`, fix, and try again.

## 4. Production

A document issued in production is legally binding and consumes a credit. Moving there is
the person's decision, made by reconnecting Stackin and choosing **Production** on the
consent screen — it is never switched from inside the conversation. Then:

1. `get_company_readiness` once — production may block on `plan`, which homologation does
   not check.
2. The real document, through `issue-invoice`, with its data confirmed.

## What not to do

- Do not loop on `get_company_readiness`. Once per change.
- Do not write an address the person has not seen and confirmed.
- Do not fill a fiscal field from a default, a suggestion or a guess.
- Do not call a homologation document an invoice the person can send to a customer.
