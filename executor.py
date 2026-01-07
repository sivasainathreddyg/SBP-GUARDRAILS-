import os
from registry import VALIDATOR_REGISTRY


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "selected_guardrails.txt")


def load_selected_validators():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as f:
        content = f.read().strip()

    if not content:
        return []

    return [v.strip().lower() for v in content.split(",")]


def execute_validators(text: str):
    selected_validators = load_selected_validators()

    results = {}
    overall_passed = True

    for name in selected_validators:
        validator = VALIDATOR_REGISTRY.get(name)

        if not validator:
            results[name] = {
                "passed": False,
                "message": "Validator not found"
            }
            overall_passed = False
            continue

        result = validator.validate(text)
        results[name] = result

        if not result.get("passed", True):
            overall_passed = False

    return {
        "overall_passed": overall_passed,
        "validators_used": selected_validators,
        "results": results
    }
