# import re
# from guardrails import Guard, OnFailAction
# from guardrails.hub import DetectPII

# class PIIDetector:
#     def __init__(self):
#         self.password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$"

#         self.guard = Guard().use(
#             DetectPII(
#                 on_fail=OnFailAction.NOOP
#             )
#         )

#     def validate(self, text: str):
#         if re.fullmatch(self.password_pattern, text):
#             return {
#                 # "status": "success",
#                 "message": "Sensitive data detected (password pattern)",
#                 "passed": True
#             }

#         result = self.guard.validate(text)

#         if result.validation_passed:
#             return {
#                 # "status": "success",
#                 "message": "No PII detected",
#                 "passed": True
#             }

#         return {
#             # "status": "success",
#             "message": "PII detected",
#             "passed": False
#         }

import re
from guardrails import Guard, OnFailAction
from guardrails.hub import DetectPII

class PIIDetector:
    def __init__(self):
        self.password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$"

        # Define ALL possible entities we can check
        self.all_entities = [
            "ADDRESS", "DATE_TIME", "EMAIL", "IP_ADDRESS", 
            "PHONE_NUMBER", "IN_AADHAAR"
        ]

        # Map user-friendly names to your entity names
        self.name_map = {
            "email": "EMAIL",
            "phone": "PHONE_NUMBER",
            "aadhaar": "IN_AADHAAR",
            "ip_address": "IP_ADDRESS",
            "date_time": "DATE_TIME",
            "address": "ADDRESS"
        }

        # Initialize with ALL entities by default
        self._initialize_guard(self.all_entities)

    def _initialize_guard(self, entities):
        """Create guard with specific entities"""
        self.guard = Guard().use(
            DetectPII(
                pii_entities=entities,
                on_fail=OnFailAction.NOOP
            )
        )
        self.current_entities = entities

    def validate(self, text: str):
        """Default: Check ALL entities"""
        return self._validate_with_entities(text, self.all_entities)

    def check_except(self, exclude_list, text: str):
        """
        Check ALL entities EXCEPT the ones in exclude_list
        exclude_list: list of things to exclude (e.g., ['email', 'phone'])
        """
        # Convert user-friendly names to entity names
        exclude_entities = []
        for item in exclude_list:
            entity = self.name_map.get(item.lower())
            if entity:
                exclude_entities.append(entity)
        # Start with all entities, remove excluded ones
        entities_to_check = []
        for entity in self.all_entities:
            if entity not in exclude_entities:
                entities_to_check.append(entity)

        # If all entities are excluded, don't run PII check
        if not entities_to_check:
            return {
                "message": "All PII types excluded - nothing to check",
                "passed": True,
                "excluded": exclude_list
            }

        return self._validate_with_entities(text, entities_to_check)

    def _validate_with_entities(self, text: str, entities_to_check):
        """Core validation logic with specific entities"""
        # Reinitialize guard if entities changed
        if entities_to_check != self.current_entities:
            self._initialize_guard(entities_to_check)

        # Check password pattern first (your existing logic)
        if re.fullmatch(self.password_pattern, text):
            return {
                "message": "PII detected ",
                "passed": False
            }

        # Run PII check with specific entities
        result = self.guard.validate(text)

        if result.validation_passed:
            return {
                "message" : "No PII detected",
                "passed": True
            }
        return {
            "message" : "PII detected",
            "passed": False
        }