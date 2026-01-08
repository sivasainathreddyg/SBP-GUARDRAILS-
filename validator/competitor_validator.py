import os
import re

class CompetitorValidator:
    def __init__(
        self,
        competitors_file="data/competitors.txt",
        sensitivity=100   # exact match by default
    ):
        self.sensitivity = sensitivity

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.competitors_path = os.path.join(base_dir, competitors_file)

        self.competitors = self._load_competitors()
        print(competitors_file)

    def _load_competitors(self):
        if not os.path.exists(self.competitors_path):
            return []

        with open(self.competitors_path, "r", encoding="utf-8") as f:
            return [
                line.strip().lower()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

    def validate(self, text: str):
        self.competitors = self._load_competitors()
        if not text or not isinstance(text, str):
            return {
                "message": "Invalid input",
                "passed": True
            }

        if not self.competitors:
            return {
                "message": "No competitors configured",
                "passed": True
            }

        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)

        for word in words:
            if word in self.competitors:
                return {
                    "message": "Competitor detected",
                    "passed": False,
                    "details": {
                        "matched_competitor": word
                    }
                }

        return {
            "message": "No competitor detected",
            "passed": True
        }
