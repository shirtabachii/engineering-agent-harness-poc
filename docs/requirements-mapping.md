# Requirements sheet → repo mapping

Quick pointer from the requirements sheet categories to where each lands in
this skeleton, and who's likely to own extending it next week.

| Sheet category | Sheet item | Where it lives today (stub) | Likely owner next week |
|---|---|---|---|
| Workflow | Trigger from Linear | `triggers/fake_linear_webhook.py` | You (Workflow & orchestration) |
| Workflow | Human-in-the-loop | Graph currently ends at `assess_finding`'s conditional edges instead of pausing for real input — needs a real interrupt/resume point | You (Workflow & orchestration) |
| Harness | Vendor-agnostic model switching | Not present yet — `assess_finding` has no model call at all today | Teammate A (Harness & sandboxing) |
| Harness | Agent sandboxing | `cluster/namespace-rbac.yaml` — minimal namespace + read-only RBAC | Teammate A (Harness & sandboxing) |
| Harness | Versioned shared skills repo | Not started | TBD |
| Infra | CI/CD lifecycle for the harness | Not started | Teammate B (Infra, credentials, monitoring) |
| Infra | Credentials management (Vault) | Not started — Job currently has no secrets at all | Teammate B (Infra, credentials, monitoring) |
| Monitoring | Traces of agent work | `graph.py` just prints JSON to stdout — no structured trace store | Teammate B (Infra, credentials, monitoring) |
| Monitoring | Cost monitoring | Not started | Teammate B (Infra, credentials, monitoring) |

Update this table as slices land — it's the fastest way for the three of you
to see what's real vs. still a stub without re-reading all the code.
