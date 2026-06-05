from app.guardrails.output_guardrails import (
    validate_output
)

def output_guardrails_node(state):

    passed, reason = validate_output(
        state["generated_answer"],
        state["retrieved_docs"]
    )

    state["output_validation_passed"] = passed

    if passed:

        state["final_response"] = (
            state["generated_answer"]
        )

    else:

        state["final_response"] = (
            f"SAFE FALLBACK: {reason}"
        )

    return state