# import os
# from registry import VALIDATOR_REGISTRY


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE = os.path.join(BASE_DIR, "data", "selected_guardrails.txt")

# SELECTED_VALIDATORS = []
# def load_selected_validators():
#     if not os.path.exists(DATA_FILE):
#         return []

#     with open(DATA_FILE, "r") as f:
#         content = f.read().strip()

#     if not content:
#         return []

#     return [v.strip().lower() for v in content.split(",")]

# # def refresh_selected_validators():
# #     global SELECTED_VALIDATORS
# #     SELECTED_VALIDATORS = load_selected_validators()
# #     print(" FastAPI loaded validators:", SELECTED_VALIDATORS)


# def execute_validators(text: str):
#     selected_validators = load_selected_validators()
#     # print("hiiiiiiiiiiiiiiii")
#     # print(SELECTED_VALIDATORS)
#     results = {}
#     overall_passed = True

#     for name in selected_validators:
#         validator = VALIDATOR_REGISTRY.get(name)

#         if not validator:
#             results[name] = {
#                 "passed": False,
#                 "message": "Validator not found"
#             }
#             overall_passed = False
#             continue

#         result = validator.validate(text)
#         results[name] = result

#         if not result.get("passed", True):
#             overall_passed = False

#     return {
#         "overall_passed": overall_passed,
#         "validators_used": selected_validators,
#         "results": results
#     }


import os
from registry import VALIDATOR_REGISTRY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MAIN_FILE = os.path.join(DATA_DIR, 'selected_guardrails.txt')

def read_validator_options(validator_name):
    """Read sub-options for a validator from its separate file"""
    options_file = os.path.join(DATA_DIR, f'{validator_name}_options.txt')

    # If file doesn't exist, return empty list (no exclusions)
    if not os.path.exists(options_file):
        return []  # Changed from None to []

    with open(options_file, 'r') as f:
        content = f.read().strip()

    # If file exists but empty, return empty list
    if not content:
        return []

    # Return list of options
    return [line.strip() for line in content.split('\n') if line.strip()]

def load_selected_validators():
    """Read main file to get list of selected validators with their options"""
    if not os.path.exists(MAIN_FILE):
        return {}

    with open(MAIN_FILE, 'r') as f:
        content = f.read().strip()

    if not content:
        return {}

    validators = {}

    # Split by comma or newline
    for item in content.replace('\n', ',').split(','):
        name = item.strip()
        if name:
            # Get options from separate file
            options = read_validator_options(name)
            validators[name] = options

    return validators

def execute_validators(text: str):
    selected_validators = load_selected_validators()

    results = {}
    overall_passed = True

    for name, options in selected_validators.items():
        validator = VALIDATOR_REGISTRY.get(name)

        if not validator:
            results[name] = {
                "passed": False,
                "message": "Validator not found"
            }
            overall_passed = False
            continue

        # SPECIAL: For PII validator
        if name == "detectpii" and hasattr(validator, 'check_except'):
            # options will be [] (empty) if no sub-options selected
            # or ['email', 'phone'] if sub-options selected
            result = validator.check_except(options, text)
        else:
            # All other validators
            result = validator.validate(text)

        results[name] = result

        if not result.get("passed", True):
            overall_passed = False

    return {
        "overall_passed": overall_passed,
        "validators_used": list(selected_validators.keys()),
        "results": results
    }
 