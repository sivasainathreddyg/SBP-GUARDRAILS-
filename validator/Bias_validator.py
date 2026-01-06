from guardrails import Guard
from guardrails.hub import BiasCheck
from guardrails import OnFailAction


class BiasValidator:
    def __init__(self, threshold=0.7):
        self.guard = Guard().use(
            BiasCheck(
                on_fail=OnFailAction.NOOP,   # IMPORTANT: API should not crash
                threshold=threshold
            )
        )

    def validate(self, text: str):
        result = self.guard.validate(text)

        if result.validation_passed:
            return {
                "message": "No bias detected",
                "passed": True
            }
        else:
            return {
                "message": "Bias detected",
                "passed": False
            }
