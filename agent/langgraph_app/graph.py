"""
Minimal LangGraph skeleton for the Engineering Agent Harness POC.

This proves the SHAPE of the CVE pilot workflow:
  gather_evidence -> assess_finding -> (no_fix_needed | escalate | prepare_fix)

Nothing here does real CVE analysis yet. Swap the node internals later;
keep this wiring stable so "workflow" and "harness internals" stay separable
pieces that different people can own.
"""
import json
import sys
from typing import Optional, TypedDict

from langgraph.graph import END, StateGraph

from nodes.assess_finding import assess_finding
from nodes.gather_evidence import gather_evidence
from nodes.prepare_fix import prepare_fix


class CVEState(TypedDict, total=False):
    cve_id: str
    advisory: dict
    dependencies: dict
    evidence: dict
    disposition: str
    fix_plan: Optional[dict]


def route_after_assessment(state: CVEState) -> str:
    return state["disposition"]


def build_graph():
    graph = StateGraph(CVEState)

    graph.add_node("gather_evidence", gather_evidence)
    graph.add_node("assess_finding", assess_finding)
    graph.add_node("prepare_fix", prepare_fix)

    graph.set_entry_point("gather_evidence")
    graph.add_edge("gather_evidence", "assess_finding")

    graph.add_conditional_edges(
        "assess_finding",
        route_after_assessment,
        {
            "no_fix_needed": END,
            "escalate": END,
            "fix_authorized": "prepare_fix",
        },
    )
    graph.add_edge("prepare_fix", END)

    return graph.compile()


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "/data/sample_cve.json"
    with open(input_path) as f:
        ticket = json.load(f)

    app = build_graph()
    result = app.invoke(
        {
            "cve_id": ticket["cve_id"],
            "advisory": ticket["advisory"],
            "dependencies": ticket["dependencies"],
        }
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
