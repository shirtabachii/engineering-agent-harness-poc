"""
Stub for: "agent prepares and tests a fix ... opens a draft PR for review."

Not implemented in this skeleton. This node exists purely so the graph's
shape matches the real pilot workflow (scope-authorized -> prepare & validate
-> draft PR). Wire in real fix-prep, isolated-workspace testing, and draft-PR
creation here once the harness/sandboxing slice is ready.
"""


def prepare_fix(state):
    return {
        "fix_plan": {
            "status": "not_implemented",
            "note": "prepare_fix stub reached — wire real fix logic here",
            "cve_id": state.get("cve_id"),
        }
    }
