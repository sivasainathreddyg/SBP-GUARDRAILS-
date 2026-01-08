# import os
# from registry import VALIDATOR_REGISTRY


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_FILE = os.path.join(BASE_DIR, "data", "selected_guardrails.txt")


# def load_selected_validators():
#     if not os.path.exists(DATA_FILE):
#         return []

#     with open(DATA_FILE, "r") as f:
#         content = f.read().strip()

#     if not content:
#         return []

#     return [v.strip().lower() for v in content.split(",")]


# def execute_validators(text: str):
#     selected_validators = load_selected_validators()

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
import re
from registry import VALIDATOR_REGISTRY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "selected_guardrails.txt")


def parse_config():
    """Parse the file with detectpii[email,phone] format"""
    if not os.path.exists(DATA_FILE):
        return {}
    
    with open(DATA_FILE, "r") as f:
        content = f.read().strip()
    
    if not content:
        return {}
    
    validators = {}
    
    # Split by lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    current_name = None
    options = []
    in_options = False
    
    for line in lines:
        # Check if line ends with '[' (start of options)
        if line.endswith('['):
            # Example: "detectpii["
            current_name = line[:-1].strip()
            options = []
            in_options = True
        
        # Check if line ends with ']' (end of options)
        elif line.endswith(']'):
            if current_name and in_options:
                # Remove ']' and add last option
                last_opt = line[:-1].rstrip(',')
                if last_opt:
                    options.append(last_opt)
                
                validators[current_name] = options
                current_name = None
                in_options = False
        
        # We're inside options block
        elif in_options:
            option = line.rstrip(',')
            if option:
                options.append(option)
        
        # Simple validator (no options)
        else:
            # Remove trailing comma if present
            name = line.rstrip(',')
            if name:
                validators[name] = []
    
    return validators


def execute_validators(text: str):
    selected_validators = parse_config()

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

        # SPECIAL: For PII validator, use check_except if options exist
        if name == "detectpii" and hasattr(validator, 'check_except'):
            result = validator.check_except(options, text)
        else:
            # All other validators use normal validate()
            result = validator.validate(text)

        results[name] = result
        if not result.get("passed", True):
            overall_passed = False

    return {
        "overall_passed": overall_passed,
        "validators_used": list(selected_validators.keys()),
        "results": results
    }