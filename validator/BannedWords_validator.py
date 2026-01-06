from rapidfuzz import process, fuzz

class KeywordMatcher:
    def __init__(self, keywords=None, sensitivity=80):
        if keywords is None:
            self.keywords = [
                "cocaine", "heroin", "meth", 
                "AK-47", "IED", "silencer", 
                "suicide", "bomb","banana"
            ]
        else:
            self.keywords = keywords

        self.keywords = [k.lower() for k in self.keywords]
        self.sensitivity = sensitivity

    def find_match(self, text):
        if not text or not isinstance(text, str):
            return False, None

        clean_text = text.lower()

        match = process.extractOne(
            query=clean_text,
            choices=self.keywords,
            scorer=fuzz.WRatio,
            score_cutoff=self.sensitivity
        )
        print(match)
        print("input",text)
        print(self.keywords)

        if match:
            term, score, _ = match

            return True, {
                "term": term,
                "score": score
            }

        return False, None