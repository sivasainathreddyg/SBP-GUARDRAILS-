# from guardrails.hub import CucumberExpressionMatch
from cucumber_expressions.parameter_type import ParameterType
from guardrails import OnFailAction
# from validator.main import CucumberExpressionMatch
from guardrails import Guard, OnFailAction
from guardrails_api_client import FailResult, PassResult
from validator.cucumber_validator import CucumberExpressionMatch



EXPRESSION = [
    "I buy {positive_number} apple(s)/banana(s)/orange(s)",
    "I sell {positive_number} apple(s)/banana(s)/orange(s)"
    ]

positive_number = ParameterType(
    "positive_number",
    regexp=r"\d+",
    type=int
)

# validator = CucumberExpressionMatch(
#     EXPRESSION,
#     parameter_types=[positive_number],
#     on_fail=OnFailAction.EXCEPTION
# )
validators = [
    CucumberExpressionMatch(
        expression=expr,
        parameter_types=[positive_number],
        on_fail=OnFailAction.NOOP  # IMPORTANT
    )
    for expr in EXPRESSION
]
def validate_user_text(user_text: str):
    """
    User can enter ANY text.
    Validation is applied ONLY if it matches the intent.
    """

    # Step 1: Check if this looks like a purchase sentence
    if not user_text.lower().startswith(("i buy", "i sell", "i return")):
        return {
            "status": "skipped",
            "reason": "Free text detected, no structured validation needed"
        }

    # Step 2: Apply cucumber validation
    # result = validator.validate(user_text)
    for validator in validators:
        result = validator.validate(user_text)

    # if result.__class__.__name__ == "PassResult":
    #     return {
    #         "status": "valid",
    #         "message": "Structured purchase statement is valid"
    #     }
        if isinstance(result, PassResult):
            return {
                "status": "valid",
                "message": "Text matches a supported structured expression"
            }

    return {
        "status": "invalid",
        "error": result.error_message,
        "suggested_fix": result.fix_value
    }
    
# val=validate_user_text("I went to the market yesterday and bought some apples")
# print(val)

user_text = input("Enter text: ")

val=validate_user_text(user_text)

print(val)


# Why NOT regex directly?
# ^I buy \d+ (apple|banana|orange)s?$
# I buy {positive_number} apple(s)/banana(s)/orange(s)



