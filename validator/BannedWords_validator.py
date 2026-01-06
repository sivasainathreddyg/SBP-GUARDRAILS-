# from rapidfuzz import process, fuzz

# class KeywordMatcher:
#     def __init__(self, keywords=None, sensitivity=80):
#         if keywords is None:
#             self.keywords = [
#                 "cocaine", "heroin", "meth", 
#                 "AK-47", "IED", "silencer", 
#                 "suicide", "bomb","banana"
#             ]
#         else:
#             self.keywords = keywords

#         self.keywords = [k.lower() for k in self.keywords]
#         self.sensitivity = sensitivity

#     def find_match(self, text):
#         if not text or not isinstance(text, str):
#             return False, None

#         clean_text = text.lower()

#         match = process.extractOne(
#             query=clean_text,
#             choices=self.keywords,
#             scorer=fuzz.WRatio,
#             score_cutoff=self.sensitivity
#         )
#         print(match)
#         print("input",text)
#         print(self.keywords)

#         if match:
#             term, score, _ = match

#             return True, {
#                 "term": term,
#                 "score": score
#             }

#         return False, None

from rapidfuzz import process, fuzz
import re

class BannedWordsValidator:
    def __init__(self, keywords=None, sensitivity=85):
        self.keywords = keywords or [
            "cocaine", "heroin", "meth",
            "ak-47", "ied", "silencer",
            "suicide", "bomb", "banana"
        ]

        self.keywords = [k.lower() for k in self.keywords]
        self.sensitivity = sensitivity

    def validate(self, text: str):
        if not text or not isinstance(text, str):
            return {
                "status": "success",
                "message": "Invalid input",
                "passed": True
            }

        words = re.findall(r"\b\w+\b", text.lower())

        for word in words:
            match = process.extractOne(
                query=word,
                choices=self.keywords,
                scorer=fuzz.WRatio,
                score_cutoff=self.sensitivity
            )

            if match:
                term, score, _ = match
                return {
                    "status": "success",
                    "message": "Banned word detected",
                    "passed": False,
                    "details": {
                        "input_word": word,
                        "matched_term": term,
                        "score": score
                    }
                }

        return {
            "status": "success",
            "message": "No banned words detected",
            "passed": True
        }
