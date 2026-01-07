# from validator.BannedWords_validator import KeywordMatcher

# def run_test():
#     matcher = KeywordMatcher()

#     text = "cocaine selling cheap"
#     found, result = matcher.find_match(text)

#     if found:
#         print(f"Match found: {result['term']} (Score: {result['score']})")
#     else:
#         print("No match found.")


# if __name__ == "__main__":
#     run_test()


from validator.BannedWords_validator import BannedWordsValidator

validator = BannedWordsValidator()

tests = [
    "I like apples",
    "This banana is tasty",
    "He planted a b0mb",
    "They used an AK47",
    "Life is beautiful"
]

for t in tests:
    print("Input:", t)
    print(validator.validate(t))
    print("-" * 50)
