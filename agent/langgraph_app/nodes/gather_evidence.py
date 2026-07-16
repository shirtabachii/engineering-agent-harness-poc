"""
Stub for: "reading the advisory, the dependency graph, and our code
to work out whether the product is affected."

Today this just reshapes the input ticket into an evidence blob.
Later: pull the real advisory text, real lockfile/dependency graph,
and real code references here.
"""


def gather_evidence(state):
    advisory = state["advisory"]
    dependencies = state["dependencies"]
    package = advisory.get("package")

    evidence = {
        "advisory_id": advisory.get("id"),
        "advisory_summary": advisory.get("summary"),
        "affected_package": package,
        "affected_versions": advisory.get("affected_versions", []),
        "our_locked_version": dependencies.get(package),
    }

    return {"evidence": evidence}
