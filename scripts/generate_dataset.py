from pathlib import Path
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(
    api_key=OPENAI_API_KEY
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASE_DIR = PROJECT_ROOT / "data" / "documents"

DOCUMENTS = {
    "engineering": [
        ("SOP-ENG-001", "Production Deployment Process"),
        ("SOP-ENG-002", "Emergency Rollback Procedure"),
        ("SOP-ENG-003", "API Versioning Standard"),
        ("SOP-ENG-004", "Feature Flag Management"),
        ("SOP-ENG-005", "Blue Green Deployment"),
        ("SOP-ENG-006", "Incident Escalation Workflow"),
        ("SOP-ENG-007", "Capacity Planning"),
        ("SOP-ENG-008", "Service Ownership Guidelines"),
        ("SOP-ENG-009", "Database Migration Procedure"),
        ("SOP-ENG-010", "Release Approval Workflow"),
    ],

    "security": [
        ("SEC-001", "Data Encryption Policy"),
        ("SEC-002", "Access Control Standard"),
        ("SEC-003", "Secrets Management Policy"),
        ("SEC-004", "Key Rotation Procedure"),
        ("SEC-005", "Vulnerability Management"),
        ("SEC-006", "Third Party Access Policy"),
        ("SEC-007", "Audit Logging Requirements"),
        ("SEC-008", "Data Retention Policy"),
        ("SEC-009", "Incident Response Standard"),
        ("SEC-010", "Secure Development Lifecycle"),
    ],

    "aws": [
        ("ARCH-001", "Inference Platform"),
        ("ARCH-002", "RAG Platform"),
        ("ARCH-003", "Multi Region Strategy"),
        ("ARCH-004", "Monitoring Architecture"),
        ("ARCH-005", "Data Lake Design"),
        ("ARCH-006", "EKS Cluster Design"),
        ("ARCH-007", "Authentication Architecture"),
        ("ARCH-008", "Vector Search Platform"),
        ("ARCH-009", "Evaluation Pipeline"),
        ("ARCH-010", "Disaster Recovery Architecture"),
    ],

    "incidents": [
        ("INC-001", "Vector Search Outage"),
        ("INC-002", "EKS Node Failure"),
        ("INC-003", "OpenAI API Latency"),
        ("INC-004", "RDS Failover Event"),
        ("INC-005", "Deployment Failure"),
        ("INC-006", "Prompt Injection Attempt"),
        ("INC-007", "Cost Spike Incident"),
        ("INC-008", "Authentication Outage"),
        ("INC-009", "Data Pipeline Failure"),
        ("INC-010", "Hallucination Regression Incident"),
    ],

    "mlops": [
        ("RUN-001", "Model Deployment"),
        ("RUN-002", "Model Rollback"),
        ("RUN-003", "Dataset Validation"),
        ("RUN-004", "Embedding Refresh"),
        ("RUN-005", "Feature Store Recovery"),
        ("RUN-006", "Evaluation Pipeline Execution"),
        ("RUN-007", "Batch Inference Process"),
        ("RUN-008", "Monitoring Alerts"),
        ("RUN-009", "Drift Detection"),
        ("RUN-010", "Golden Dataset Update"),
    ],

    "product": [
        ("PRD-001", "AetherAI Gateway"),
        ("PRD-002", "Enterprise RAG Service"),
        ("PRD-003", "Prompt Management Platform"),
        ("PRD-004", "Evaluation Engine"),
        ("PRD-005", "Model Registry"),
        ("PRD-006", "Guardrails Gateway"),
        ("PRD-007", "Agent Workflow Studio"),
        ("PRD-008", "Analytics Dashboard"),
        ("PRD-009", "Knowledge Hub"),
        ("PRD-010", "Reliability Platform"),
    ],
}


BASE_SYSTEM_PROMPT = """
You are a senior enterprise architect working at AetherAI Cloud.

Generate realistic internal enterprise documentation.

Requirements:
- 800 to 1200 words
- Production-grade language
- AWS terminology
- Detailed and unique
- No placeholders
- No markdown
- No generic filler content

Company:
- Enterprise RAG Platform
- LLM Gateway
- AI Reliability Platform
- Evaluation Pipelines
- AWS-hosted AI Infrastructure
"""


CATEGORY_PROMPTS = {
    "engineering": """
Create a Standard Operating Procedure.

Sections:
1. Document ID
2. Title
3. Purpose
4. Scope
5. Prerequisites
6. Technical Details
7. Step-by-Step Procedure
8. Failure Handling
9. Risks
10. Compliance Considerations
11. Summary
""",

    "security": """
Create a Security Policy document.

Sections:
1. Policy ID
2. Title
3. Objective
4. Scope
5. Policy Statements
6. Security Controls
7. Monitoring
8. Exceptions
9. Compliance Requirements
10. Enforcement
11. Summary
""",

    "aws": """
Create an AWS Architecture document.

Sections:
1. Architecture ID
2. Title
3. Business Requirements
4. Architecture Overview
5. AWS Services Used
6. Data Flow
7. Availability Design
8. Security Design
9. Cost Optimization
10. Disaster Recovery
11. Summary
""",

    "incidents": """
Create a realistic Incident Report.

Sections:
1. Incident ID
2. Title
3. Severity
4. Timeline
5. Impact
6. Root Cause Analysis
7. Resolution
8. Preventive Actions
9. Lessons Learned
10. Summary
""",

    "mlops": """
Create an MLOps Runbook.

Sections:
1. Runbook ID
2. Title
3. Purpose
4. Prerequisites
5. Operational Procedure
6. Monitoring
7. Recovery Steps
8. Validation
9. Risks
10. Summary
""",

    "product": """
Create a Product Documentation document.

Sections:
1. Product ID
2. Product Overview
3. Customer Problems
4. Key Features
5. Architecture
6. Usage Workflow
7. Limitations
8. Security Considerations
9. Roadmap
10. Summary
"""
}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2)
)
def generate_document(
    doc_id: str,
    title: str,
    category: str
) -> str:

    prompt = f"""
Generate a realistic enterprise document.

Category: {category}

Document ID: {doc_id}

Title: {title}

{CATEGORY_PROMPTS[category]}

Generate a realistic enterprise document for AetherAI Cloud.
"""

    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {
                "role": "system",
                "content": BASE_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.output_text


def save_document(
    category: str,
    doc_id: str,
    content: str
):

    folder = BASE_DIR / category

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = folder / f"{doc_id}.txt"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


def main():

    total = 0

    for category, docs in DOCUMENTS.items():

        for doc_id, title in docs:

            print(
                f"Generating {doc_id}..."
            )

            content = generate_document(
                doc_id,
                title,
                category
            )

            save_document(
                category,
                doc_id,
                content
            )

            total += 1

    print(
        f"\nGenerated {total} documents."
    )


if __name__ == "__main__":
    main()