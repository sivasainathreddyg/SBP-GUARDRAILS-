import re
from guardrails import Guard, OnFailAction
from guardrails.hub import DetectPII

class PIIDetector:
    def __init__(self):
        self.password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$"

        self.guard = Guard().use(
            DetectPII(
                on_fail=OnFailAction.NOOP
            )
        )

    def validate(self, text: str):
        # 1️⃣ Password regex check
        if re.fullmatch(self.password_pattern, text):
            return {
                "status": "success",
                "message": "Sensitive data detected (password pattern)",
                "passed": False
            }

        # 2️⃣ PII check
        result = self.guard.validate(text)

        if result.validation_passed:
            return {
                "status": "success",
                "message": "No PII detected",
                "passed": True
            }

        return {
            "status": "success",
            "message": "PII detected",
            "passed": False
        }
