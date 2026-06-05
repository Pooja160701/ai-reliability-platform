import re


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "disregard previous instructions",
    "reveal system prompt",
    "show system prompt",
    "forget your instructions"
]


JAILBREAK_PATTERNS = [
    "developer mode",
    "dan",
    "do anything now",
    "pretend you are unrestricted",
    "act without limitations"
]


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

PHONE_PATTERN = r"\b\d{10}\b"

CREDIT_CARD_PATTERN = r"\b(?:\d[ -]*?){13,16}\b"


def detect_prompt_injection(text: str) -> bool:
    text = text.lower()

    return any(
        pattern in text
        for pattern in PROMPT_INJECTION_PATTERNS
    )


def detect_jailbreak(text: str) -> bool:
    text = text.lower()

    return any(
        pattern in text
        for pattern in JAILBREAK_PATTERNS
    )


def detect_pii(text: str) -> bool:

    if re.search(EMAIL_PATTERN, text):
        return True

    if re.search(PHONE_PATTERN, text):
        return True

    if re.search(CREDIT_CARD_PATTERN, text):
        return True

    return False


def validate_input(text: str) -> tuple[bool, str]:

    if detect_prompt_injection(text):
        return False, "Prompt injection detected"

    if detect_jailbreak(text):
        return False, "Jailbreak attempt detected"

    if detect_pii(text):
        return False, "PII detected"

    return True, "Input validated"