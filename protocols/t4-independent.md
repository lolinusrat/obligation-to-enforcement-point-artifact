# T4 extension study — independent pass

**Written against the sealed case file** (`t4-cases.json`, `09fcf770…`) without reopening the derivation
pass (`t4-derivations.md`, sealed at 10:14 UTC). For each case: what an architect should build, argued
from the estate, and whether the obligation is then adequately enforceable on every path. Outcome codes
as in protocol §5: F (every path enforceable), A (enforceable or adequately approximated, with an
explicit residual), U (some path not adequately enforceable in the modelled architecture).

## C1

Two egress routes exist and neither control sees the other's traffic, so both must enforce. The proxy
may inspect tool traffic and can check signed request metadata, so the same two assertions the gateway
uses — the data layer's sensitivity label and the business context's purpose attestation — can be
attached to tool calls and checked there. Both routes can then block before disclosure. **Build:**
gateway and proxy, one shared issuer and policy for both assertions. **F.**

## C2

The tool route is opaque: the proxy sees destinations only. It cannot tell sensitive from
non-sensitive payloads, so the only preventive option is to refuse tool egress to any destination not on
the allow-list, and the case says that is acceptable. **Build:** gateway as C1; destination allow-list at
the proxy. This is adequate only to the extent the allow-list holds no external destination that could
receive sensitive data; anything sent to an allow-listed external endpoint is unchecked for sensitivity
and purpose. **A**, with that residual stated.

## C3

The gateway enforces model calls. Pasting from an unmanaged device crosses no location the enterprise
controls; nothing in the modelled architecture can see or stop it. **Build:** gateway only; state the
unmanaged-device route as unenforceable here (policy, device management or data-access controls upstream
are redesigns outside the model). **U.**

## C4

Each store is the only control its path passes, so both must decide. The primary store already holds the
collection purpose; the index does not, because ingestion dropped it. The purpose attestation can be
sent to both. **Build:** propagate the collection-purpose label into the index and check the attestation
at both stores. One practical point the facts force: entries already in the index have no label, so
until they are re-ingested with labels the index must refuse unlabelled entries. With that, both paths
are enforced. **F.**

## C5

The SDK path is controlled by the orchestrator itself. The direct path reaches the service without the
orchestrator; the service can deny but does not know the task. The orchestrator can issue a scoped
capability token that the service checks. **Build:** orchestrator enforcement on SDK calls; service
requires a valid task-scoped token on direct calls. **F.**

## C6

Chat output can be filtered at its endpoint. Batch mail passes an appliance that can see toxicity but
cannot act or emit a verdict, and a relay that can block but cannot see content. No location on that
route can both decide and act, blocking all batch mail is not acceptable, and toxic mail once delivered
cannot be recalled. **Build:** filtering endpoint for chat; batch mail remains uncontrolled for toxicity
unless the architecture changes (route batch generation through the filtering endpoint). **U.**

## C7

Hosted-model use passes the gateway; local use happens on managed workstations whose endpoint agent can
see what runs and terminate it. Both know which model is in use; neither knows the register, which can
be pushed to both. **Build:** gateway and endpoint agent, both checking the same register. **F.**

## C8

Gateway calls can carry the requester's identity. Raw egress from the batch service is opaque, so the
relay can record that a call happened and which workload made it, not which user it was for; the case
accepts proxy recording. **Build:** gateway records requester; relay records workload identity. The
obligation is not fully met for batch calls — requester attribution is missing unless correlated later
with the batch service's own records. **A**, with that residual.

## Summary (machine-read by `extract.py`)

| case | independent outcome | set |
|---|---|---|
| C1 | F | Z4, Z7 |
| C2 | A | Z4, Z7 |
| C3 | U | Z4 |
| C4 | F | Z6a, Z6b |
| C5 | F | Z3, Z6 |
| C6 | U | Z5a |
| C7 | F | Z4, Z8 |
| C8 | A | Z4, Z7 |
