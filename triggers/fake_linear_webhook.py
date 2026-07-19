"""
Simulates "a CVE arrives in Linear." In the real pilot this would be a
Linear webhook (or an OpenSWE trigger). For the POC this script:

  1. writes a sample CVE ticket into a ConfigMap manifest
  2. applies that ConfigMap + the agent Job to the kind cluster

Usage:
    python3 fake_linear_webhook.py [path/to/cve.json]
"""
import json
import subprocess
import sys
import tempfile
import textwrap

DEFAULT_CVE = {
    "cve_id": "CVE-2026-99999",
    "advisory": {
        "id": "CVE-2026-99999",
        "summary": "Example: fabricated vulnerability in demo-package, POC use only",
        "package": "demo-package",
        "affected_versions": ["1.2.0", "1.2.1"],
    },
    "dependencies": {
        "demo-package": "1.2.0",
    },
}


def main():
    cve_path = sys.argv[1] if len(sys.argv) > 1 else None
    ticket = DEFAULT_CVE
    if cve_path:
        with open(cve_path) as f:
            ticket = json.load(f)

    json_block = textwrap.indent(json.dumps(ticket, indent=2), "    ")
    configmap_yaml = (
        "apiVersion: v1\n"
        "kind: ConfigMap\n"
        "metadata:\n"
        "  name: sample-cve\n"
        "  namespace: agent-harness\n"
        "data:\n"
        "  sample_cve.json: |\n"
        f"{json_block}\n"
    )

    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
        f.write(configmap_yaml)
        configmap_path = f.name

    print(f"Writing ConfigMap manifest to {configmap_path}")
    subprocess.run(["kubectl", "apply", "-f", configmap_path], check=True)

    print("Removing any previous run, then applying agent Job...")
    subprocess.run(
        ["kubectl", "-n", "agent-harness", "delete", "job", "cve-harness-run", "--ignore-not-found"],
        check=True,
    )
    subprocess.run(["kubectl", "apply", "-f", "k8s/agent-job.yaml"], check=True)

    print("Done. Watch it with: kubectl -n agent-harness logs -f job/cve-harness-run")


if __name__ == "__main__":
    main()
