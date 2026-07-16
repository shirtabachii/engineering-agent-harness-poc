"""
Stub for: "agent works out whether we are affected and how risky the fix is."

Today this is a dumb version-string comparison — good enough to prove the
graph's shape and routing. Replace with a real semver-range check (or an
LLM call over the evidence) once the skeleton runs end-to-end.
"""


def assess_finding(state):
    evidence = state["evidence"]
    locked_version = evidence.get("our_locked_version")
    affected_versions = evidence.get("affected_versions", [])

    if locked_version is None:
        disposition = "no_fix_needed"
    elif locked_version in affected_versions:
        # Toy "risk" proxy: a narrow affected range is treated as a bounded,
        # authorizable fix; a wide range gets escalated for manual triage —
        # same shape as the "Uncertain -> Escalated" branch in the diagram.
        disposition = "fix_authorized" if len(affected_versions) <= 3 else "escalate"
    else:
        disposition = "no_fix_needed"

    return {"disposition": disposition}
