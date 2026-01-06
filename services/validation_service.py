from validator.BannedWords_validator import KeywordMatcher
from validator.HasValidURL import URLValidator

class ValidationService:
    def __init__(self):
        self.validators = [
            ("banned", KeywordMatcher()),
            ("url", URLValidator())
        ]

    def run_all(self, text):
        results = {}

        for name, validator in self.validators:
            matched, details = validator.find_match(text)
            results[name] = {
                "matched": matched,
                "details": details
            }

        return results
