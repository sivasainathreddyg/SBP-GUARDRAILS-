from guardrails import Guard, OnFailAction
from guardrails.hub import ProfanityFree

class ProfanityValidator:
    def __init__(self, threshold=0.9):
        self.guard = Guard().use(
            ProfanityFree(
                threshold=threshold,
                on_fail=OnFailAction.NOOP
            )
        )

    def validate(self, text: str):
        result = self.guard.validate(text)

        if result.validation_passed:
            return {
                "status": "success",
                "message": "No profanity detected",
                "passed": True
            }

        return {
            "status": "success",
            "message": "Profanity detected",
            "passed": False
        }
