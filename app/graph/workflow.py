from langgraph.graph import (
    StateGraph,
    END
)

from app.graph.state import GraphState

from app.graph.nodes.input_guardrails_node import (
    input_guardrails_node
)

from app.graph.nodes.retrieve_node import (
    retrieve_node
)

from app.graph.nodes.generate_node import (
    generate_node
)

from app.graph.nodes.critic_node import (
    critic_node
)

from app.graph.nodes.rewrite_node import (
    rewrite_node
)

from app.graph.nodes.output_guardrails_node import (
    output_guardrails_node
)


builder = StateGraph(GraphState)


builder.add_node(
    "input_guardrails",
    input_guardrails_node
)

builder.add_node(
    "retrieve",
    retrieve_node
)

builder.add_node(
    "generate",
    generate_node
)

builder.add_node(
    "critic",
    critic_node
)

builder.add_node(
    "rewrite",
    rewrite_node
)

builder.add_node(
    "output_guardrails",
    output_guardrails_node
)


builder.set_entry_point(
    "input_guardrails"
)


builder.add_edge(
    "input_guardrails",
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "generate"
)

builder.add_edge(
    "generate",
    "critic"
)


def critic_router(state):

    if (
        state["critic_decision"]
        == "approve"
    ):
        return "approve"

    if (
        state["retry_count"]
        >= 2
    ):
        return "fallback"

    return "rewrite"


builder.add_conditional_edges(
    "critic",
    critic_router,
    {
        "approve":
            "output_guardrails",

        "rewrite":
            "rewrite",

        "fallback":
            "output_guardrails"
    }
)


builder.add_edge(
    "rewrite",
    "retrieve"
)


builder.add_edge(
    "output_guardrails",
    END
)


graph = builder.compile()