from app.guardrails.output_guardrails import (
    validate_output
)

print(
    validate_output(
        "This diagnosis requires treatment",
        [{"content":"test"}]
    )
)