from app.evaluation.metrics import *

results = [
    {
        "critic_decision": "approve",
        "retry_count": 0
    },
    {
        "critic_decision": "approve",
        "retry_count": 1
    },
    {
        "critic_decision": "reject",
        "retry_count": 2
    }
]

print(
    "Accuracy:",
    calculate_accuracy(results)
)

print(
    "Groundedness:",
    calculate_groundedness(results)
)

print(
    "Approval:",
    calculate_approval_rate(results)
)

print(
    "Failure:",
    calculate_failure_rate(results)
)

print(
    "Retries:",
    calculate_average_retries(results)
)