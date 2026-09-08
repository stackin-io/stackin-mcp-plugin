---
name: invalidate-numbering
description: Declare an NF-e numbering range that was reserved and never used, so the gap is explained to the SEFAZ.
---

# Invalidating a numbering range

NF-e numbering has to be continuous. When a number is burned without ever being authorized —
a failed transmission, a system that reserved and crashed — the gap is explained to the SEFAZ
with an invalidation, not with a filler document.

NF-e only. NFS-e numbering is the municipality's problem, not this one's.

## Irreversible, and it burns numbers

A number declared unused can never be used. The range is **inclusive**: `10` to `12` is three
numbers, not two. One digit wrong and the company loses numbers it still needed, permanently.

## Order

1. Confirm with the person which series and which range, and read it back as a count: "series
   1, numbers 10 through 12 — three numbers, correct?"
2. Confirm none of them was authorized. An authorized document is **cancelled**, never
   invalidated; `consult_invoice` settles it when there is any doubt.
3. `invalidate_numbering`, with the reason in the person's own words — 15 to 255 characters,
   and it reaches the tax authority verbatim. The series is a string, not a number: `"1"`,
   and the range is refused before transmission if it runs backwards.

## What not to do

- Do not infer the range from a gap you noticed in `list_invoices`. A gap can also be a
  document that exists and simply was not listed on the page you read.
- Do not invalidate to "clean up" numbering. It is a declaration to the fisco, not
  housekeeping.
- Do not use it on a rejected document. A rejection did not consume the number.
