# T4 extension study — derivation pass

**Written against the sealed protocol** (`t4-protocol.md`, SHA-256 `faa7f36a…`; `t4-cases.json`,
`09fcf770…`) and sealed in turn before the independent pass began. This file applies the T4 rule of
protocol §2 to the case facts and nothing else. It records what the rule returns, not what the
architecture ought to be.

Notation: T1 (native), T2 fact, T2 verdict, T3 (approximate), as in Table 3. For each path, the
locations it traverses are tried in turn; the first that is enforced is assigned, otherwise the first
that can approximate.

## C1 — disclosure; tool calls via the web proxy, model calls via the gateway's private link

- **p1_model_call → Z4.** Missing sens (source Z6, may cross; Z4 can receive) → T2 fact; purp (judgement
  at Z2, verdict may cross) → T2 verdict; ext native → T1; block ∈ α(Z4). **Enforced.**
- **p2_agent_tool_http → Z7.** Same facts; Z7 can receive → T2 fact, T2 verdict, T1; block ∈ α(Z7).
  **Enforced.**
- **Set** {Z4, Z7}. **Consistency obligations:** the sensitivity label and the purpose attestation each
  reach two controls; both must use the same issuer, binding, validity and policy version.
- **Outcome F.**

## C2 — as C1, tool traffic opaque to the proxy

- **p1 → Z4.** As C1. **Enforced.**
- **p2 → Z7.** Z7 cannot receive assertions, so sens and purp cannot be transported; not enforced. Z7
  has block; both have a proxy; over-approximation is acceptable on p2. **Approximated** — block tool
  egress to any non-allow-listed destination, treating all tool payloads as sensitive.
- **Set** {Z4, Z7}. **Residual:** the functional cost of over-blocking tool traffic; no disclosure path
  is left unenforced.
- **Outcome A.**

## C3 — disclosure; unmanaged personal device

- **p1 → Z4.** As C1. **Enforced.**
- **p2_unmanaged_device.** Traverses no location in *L*. **Residual.**
- **Set** {Z4}. **Residual:** disclosure from an unmanaged device.
- **Outcome U.**

## C4 — purpose limitation; primary store and a vector index built earlier

- **p1_primary_store → Z6a.** pd, cpur, compat native; cur (judgement at Z2, verdict may cross) → T2
  verdict; deny ∈ α. **Enforced.**
- **p2_vector_index → Z6b.** pd, compat native; cpur (source Z6a, may cross; Z6b can receive) → T2 fact,
  carried into the index at ingestion; cur → T2 verdict; deny ∈ α. **Enforced.**
- **Set** {Z6a, Z6b}. **Consistency obligations:** the purpose attestation reaches both stores; the
  collection-purpose label in the index must be bound to the record it was copied from.
- **Outcome F.**

## C5 — task scope; SDK tool calls and direct API calls

- **p1_sdk_tool_call → Z3.** scope and call native; deny ∈ α. **Enforced** (T1).
- **p2_direct_api_call → Z6.** call native; scope (judgement at Z3, verdict may cross; Z6 can receive) →
  T2 verdict, a capability token; deny ∈ α. **Enforced.**
- **Set** {Z3, Z6}. **Consistency obligation:** Z6 must accept only tokens issued by the orchestrator
  that also governs p1, for the same task.
- **Outcome F.**

## C6 — toxic output; chat endpoint, vendor appliance and mail relay

- **p1_chat → Z5a.** tox native; block ∈ α. **Enforced.**
- **p2_batch_mail.** Z5b holds tox but can only log. Z7 can block but lacks tox, and tox may not cross
  from the appliance. Approximation: Z7 has block and tox has a proxy, but over-approximation is not
  acceptable on p2 and the effect is irreversible, so later detection does not substitute. **Residual.**
- **Set** {Z5a}. **Residual:** toxic output in batch mail. {Z5a, Z7} covers both paths, but the
  location on p2 that can act cannot decide, and the one that can decide cannot act.
- **Outcome U.**

## C7 — registered models only; hosted and local

- **p1_hosted_model → Z4.** model native; registered (source Z1, may cross; Z4 can receive) → T2 fact;
  block ∈ α. **Enforced.**
- **p2_local_model → Z8.** model native; registered → T2 fact; block ∈ α(Z8). **Enforced.**
- **Set** {Z4, Z8}. **Consistency obligation:** both enforce against the same registry version.
- **Outcome F.**

## C8 — record requester identity; gateway and raw egress

- **p1_gateway → Z4.** call native; reqid (source Z2, may cross; Z4 can receive) → T2 fact; record ∈ α.
  **Enforced.**
- **p2_raw_egress → Z7.** Z7 cannot receive assertions, so reqid cannot be transported; not enforced. Z7
  can record; reqid has a proxy (workload identity); proxy recording is acceptable on p2.
  **Approximated.**
- **Set** {Z4, Z7}. **Residual:** batch calls are attributed to the workload, not the requesting user.
- **Outcome A.**

## D0 — K6 (diagnostic; not counted)

- **p1_release → Z7.** provenance (source Z3, may cross; Z7 can receive) → T2 fact; block ∈ α.
  **Enforced.**
- **p2_third_party_republication.** No location in *L*. **Residual.**
- **Outcome U.** T4 now localises K6's gap to the re-publication path rather than reporting the
  obligation as a whole as unrouted.

## Summary (machine-read by `extract.py`)

| case | path | assigned | outcome |
|---|---|---|---|
| C1 | p1_model_call | Z4 | enforced |
| C1 | p2_agent_tool_http | Z7 | enforced |
| C2 | p1_model_call | Z4 | enforced |
| C2 | p2_agent_tool_http | Z7 | approximated |
| C3 | p1_model_call | Z4 | enforced |
| C3 | p2_unmanaged_device | — | residual |
| C4 | p1_primary_store | Z6a | enforced |
| C4 | p2_vector_index | Z6b | enforced |
| C5 | p1_sdk_tool_call | Z3 | enforced |
| C5 | p2_direct_api_call | Z6 | enforced |
| C6 | p1_chat | Z5a | enforced |
| C6 | p2_batch_mail | — | residual |
| C7 | p1_hosted_model | Z4 | enforced |
| C7 | p2_local_model | Z8 | enforced |
| C8 | p1_gateway | Z4 | enforced |
| C8 | p2_raw_egress | Z7 | approximated |
| D0 | p1_release | Z7 | enforced |
| D0 | p2_third_party_republication | — | residual |
