from typing import TypedDict
from typing import List
from typing import Optional


class GraphState(TypedDict):

    question: str

    retrieved_docs: List[str]

    generated_answer: str

    critic_decision: str

    critic_reason: str

    rewritten_query: str

    retry_count: int

    final_response: str

    input_validation_passed: bool

    output_validation_passed: bool