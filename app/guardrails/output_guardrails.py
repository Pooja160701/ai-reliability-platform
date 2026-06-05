from app.guardrails.policy_engine import load_policies

POLICIES = load_policies()

COMPETITORS = [
    "openai",
    "anthropic",
    "google",
    "microsoft",
    "cohere"
]

TOXIC_TERMS = [
    "hate",
    "kill",
    "violence"
]

MEDICAL_TERMS = [
    "diagnosis",
    "prescription",
    "treatment",
    "medical advice"
]

def detect_toxicity(text):

    text = text.lower()

    return any(
        term in text
        for term in TOXIC_TERMS
    )

def detect_competitor_content(text):

    text = text.lower()

    return any(
        competitor in text
        for competitor in COMPETITORS
    )

def detect_medical_content(text):

    text = text.lower()

    return any(
        term in text
        for term in MEDICAL_TERMS
    )

def validate_sources(retrieved_docs):

    return len(retrieved_docs) > 0

def validate_output(
    answer,
    retrieved_docs
):
    
    if detect_toxicity(answer):

        return (
            False,
            "Toxic content detected"
        )

    if (
        POLICIES["block_competitor_discussion"]
        and
        detect_competitor_content(answer)
    ):

        return (
            False,
            "Competitor discussion blocked"
        )           

    if (
        not POLICIES["allow_medical"]
        and
        detect_medical_content(answer)
    ):

        return (
            False,
            "Medical content blocked"
        )

    if (
        POLICIES["require_sources"]
        and
        not validate_sources(
            retrieved_docs
        )
    ):

        return (
            False,
            "Sources required"
        )

    return (
        True,
        "Output validated"
    )