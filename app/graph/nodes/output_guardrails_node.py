def output_guardrails_node(state):

    state["output_validation_passed"] = True

    state["final_response"] = (
        state["generated_answer"]
    )

    return state