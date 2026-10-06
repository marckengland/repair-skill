# 5 Whys: doing it right in a codebase

The 5 Whys funnel narrows from a visible symptom to an actionable root cause:

| Why | Purpose | Typical software answer |
|-----|---------|-------------------------|
| 1st | Identify the first cause contributing to the problem | "`total` is `NaN`" |
| 2nd | Dig deeper: why did the first cause occur? | "`price` is `undefined` for some items" |
| 3rd | Keep drilling down to deeper reasons | "Items from the v2 API use `unitPrice`, not `price`" |
| 4th | Reveal the underlying system or process issue | "API responses are used untyped; nothing validates their shape" |
| 5th | Reach the actionable root cause and plan corrective actions | "Add a schema/adapter at the API boundary mapping both versions to one type" |

Fixing at Why 1 (`total || 0`) hides the bug and produces wrong totals: the
next link in the chain. Fixing at Why 5 removes the whole class of bug.

## Common mistakes and how to avoid them

### 1. Guessing instead of observing
Each why is a hypothesis until evidence confirms it. Read the code path, print
the value, check the log, run the test. Write the evidence next to each answer.
If you can't get evidence, label the step **unverified** and say so.

### 2. Stopping at a symptom
"The value was null" is a symptom. Ask why it was null. A good stopping point
is a cause that is (a) within your control and (b) would have prevented the
problem if it had been different.

### 3. Going past what you control
"Because the third-party API changed" is real, but you can't fix their API.
Step back one level to what you control: "we don't validate the response
shape", "we don't pin the API version".

### 4. Blaming a person or "flakiness"
"The developer forgot" or "the test is flaky" ends the inquiry without finding
a mechanism. Ask instead: what made forgetting possible? Why is the test
nondeterministic (time, ordering, shared state, network, randomness)?

### 5. Forcing a single straight line
Real failures often have several contributing causes. When a why has two
honest answers, branch and follow both. The fix may need to address more than
one branch, or you report the others as follow-up.

### 6. Treating "5" as a rule
Stop at 3 if you've reached an actionable root cause. Go to 7 if you haven't.

### 7. Skipping the reverse check
Read the chain from the bottom up, joining each step with "therefore":

> No schema at the API boundary, **therefore** v2 items reach the cart with
> `unitPrice` instead of `price`, **therefore** `price` is undefined,
> **therefore** `total` is `NaN`.

If any "therefore" doesn't follow, a link is missing or wrong.

### 8. Confusing correlation with cause
"It started failing after commit X" tells you where to look, not why. Use
`git bisect` and diffs to locate it, then explain the mechanism.

### 9. Not testing the conclusion
A root cause is confirmed when you can **predict** behavior from it: "if this
is the cause, then input Y should also fail". Try Y. And the fix must make the
repro pass.

## Worked example

```
Problem: Checkout returns HTTP 500 for ~3% of orders since Monday.
Why 1:   OrderService.total() throws TypeError: cannot read 'amount' of null.
         Evidence: stack trace in logs, order_service.ts:88
Why 2:   order.discount is null for those orders; the code assumes an object.
         Evidence: printed failing orders; all have discount = null
Why 3:   Monday's migration made discount nullable; previously default {amount: 0}.
         Evidence: migrations/2026_10_05_discount.sql, git log
Why 4:   The ORM model type still declares discount as non-null, so the
         compiler never flagged the unsafe access.
         Evidence: models/order.ts:14 `discount: Discount`
Why 5:   Model types are hand-written and not regenerated from the schema
         after migrations.
Fix at:  Why 4 now: make the type `Discount | null` and handle null at every
         use (Phase 3 found 6 consumers). Why 5 reported as follow-up:
         generate model types from the schema in CI.
Reverse: types hand-written → type stayed non-null after migration →
         compiler missed null access → null discount crashes total() → 500.
```

Note that fixing only Why 1 (`order.discount?.amount ?? 0` at line 88) would
leave five other consumers crashing on the same null: the classic chain.
