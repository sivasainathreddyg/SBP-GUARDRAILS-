# from guardrails import Guard # type: ignore
# from guardrails.hub import ProfanityFree # type: ignore
# try:
#   # Create a guard with profanity filter
#   guard = Guard().use(ProfanityFree(on_fail="exception",threshold=0.9))  

#   # Suppose LLM returns a message
#   output = "You are a stupid person!"

#   res = guard.validate(output)  # This will raise or fail because profanity found

#   print(res.validation_passed)

# except Exception as e:
#   print(e)

from validator.profanity_validator import ProfanityValidator

validator = ProfanityValidator()

texts = [
    "You are a nice person",
    "You are stupid",
    "What the hell is this",
    "Have a great day"
]

for text in texts:
    result = validator.validate(text)
    print(f"Input: {text}")
    print(result)
    print("-" * 40)
