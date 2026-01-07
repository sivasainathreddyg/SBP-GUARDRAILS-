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
import os

class BannedWordsValidator:
    def __init__(self, keywords=None, sensitivity=80 ,words_file="data/BannedWordsList.txt"):
        # self.keywords = keywords or [
        #     "cocaine", "heroin", "meth",
        #     "ak-47", "ied", "silencer",
        #     "suicide", "bomb", "banana"
        # ]

        # self.keywords = [k.lower() for k in self.keywords]
        # self.sensitivity = sensitivity
        self.sensitivity = sensitivity

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.words_path = os.path.join(base_dir, words_file)

        self.keywords = self._load_banned_words()
        
    def _load_banned_words(self):
        if not os.path.exists(self.words_path):
            return []

        with open(self.words_path, "r", encoding="utf-8") as f:
            return [
                line.strip().lower()
                for line in f
                if line.strip() and not line.startswith("#")
            ]

    def validate(self, text: str):
        if not text or not isinstance(text, str):
            return {
                "message": "Invalid input",
                "passed": True
            }
        if not self.keywords:
            return {
                "message": "No banned words configured",
                "passed": True
            }

        words = re.findall(r"\b\w+\b", text.lower())

        for word in words:
            match = process.extractOne(
                query=word,
                choices=self.keywords,
                # scorer=fuzz.WRatio,
                scorer=fuzz.token_set_ratio,
                score_cutoff=self.sensitivity
            )

            if match:
                term, score, _ = match
                return {
                    
                    "message": "Banned word detected",
                    "passed": False,
                    "details": {
                        "input_word": word,
                        "matched_term": term,
                        "score": score
                    }
                }

        return {
            
            "message": "No banned words detected",
            "passed": True
        }
