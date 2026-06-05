import statistics


def calculate_accuracy(results):

    total = len(results)

    if total == 0:
        return 0

    correct = sum(
        1
        for result in results
        if result["critic_decision"] == "approve"
    )

    return round(
        correct / total,
        4
    )


def calculate_groundedness(results):

    total = len(results)

    if total == 0:
        return 0

    grounded = sum(
        1
        for result in results
        if result["critic_decision"] == "approve"
    )

    return round(
        grounded / total,
        4
    )


def calculate_approval_rate(results):

    total = len(results)

    if total == 0:
        return 0

    approved = sum(
        1
        for result in results
        if result["critic_decision"] == "approve"
    )

    return round(
        approved / total,
        4
    )


def calculate_failure_rate(results):

    total = len(results)

    if total == 0:
        return 0

    failed = sum(
        1
        for result in results
        if result["critic_decision"] == "reject"
    )

    return round(
        failed / total,
        4
    )


def calculate_average_retries(results):

    retries = [
        result.get(
            "retry_count",
            0
        )
        for result in results
    ]

    if not retries:
        return 0

    return round(
        statistics.mean(retries),
        2
    )