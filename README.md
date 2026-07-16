# Engineering Agent Harness — POC skeleton

**What this proves:** the shape of the Fire and Motion CVE pilot workflow —
a fake CVE ticket goes in, a LangGraph agent runs inside a kind cluster,
a disposition (`no_fix_needed` / `escalate` / `fix_authorized`) comes out.

**What this does NOT do (on purpose, for now):**
- No real Linear/OpenSWE integration — `triggers/fake_linear_webhook.py` fakes the trigger
- No real CVE/dependency analysis — `assess_finding` is a dumb version-string check
- No real sandbox isolation guarantees — RBAC is minimal-but-real, that's it
- No real fix/PR creation — `prepare_fix` is a stub

Swap these node-by-node later. Keep the graph wiring (`agent/langgraph_app/graph.py`)
and the k8s shape (`k8s/`, `cluster/`) stable — that's the part the team shares.

## Quickstart

```bash
# 1. create the local cluster
kind create cluster --config cluster/kind-config.yaml

# 2. create namespace + minimal RBAC
kubectl apply -f cluster/namespace-rbac.yaml

# 3. build the agent image and load it into kind
docker build -t agent-harness-poc:local ./agent
kind load docker-image agent-harness-poc:local

# 4. fire the fake trigger (this applies the ConfigMap + Job)
python3 triggers/fake_linear_webhook.py

# 5. watch it run
kubectl -n agent-harness logs -f job/cve-harness-run
```

Expected output: a JSON blob with `evidence` and a `disposition` field.

## Repo map

```
cluster/      kind cluster config + namespace/RBAC
agent/        the LangGraph app (Dockerized)
triggers/     stand-in for "a CVE arrives in Linear"
k8s/          Job manifest that runs the agent in-cluster
docs/         requirements → repo mapping, workflow diagram
```

## Where this maps to the requirements sheet

See `docs/requirements-mapping.md`.
