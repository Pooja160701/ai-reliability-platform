from app.guardrails.input_guardrails import validate_input


def input_guardrails_node(state):

    passed, message = validate_input(
        state["question"]
    )

    state["input_validation_passed"] = passed

    if not passed:

        state["final_response"] = message

    return state