from pathlib import Path
import yaml


POLICY_FILE = Path(__file__).parent / "policies.yaml"


def load_policies() -> dict:
    """
    Load guardrail policies from YAML file.
    """

    with open(POLICY_FILE, "r", encoding="utf-8") as file:
        policies = yaml.safe_load(file)

    return policies