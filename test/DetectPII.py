# import re
# from guardrails import Guard
# from guardrails.hub import DetectPII
 
# password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$"
 
# guard = Guard().use(
#     DetectPII(on_fail="exception")
# )
 
# def is_sensitive(text):
#     """
#     Returns True if the input contains PII or matches password regex.
#     Returns False if input is safe.
#     """
#     if re.fullmatch(password_pattern, text):
#         return True
 
#     try:
#         guard.validate(text)
#         return False  
#     except Exception:
#         return True  
       
# text = input("Enter input: ")
# print(is_sensitive(text))


from validator.pii_validator import PIIDetector

validator = PIIDetector()

tests = [
    "Hello how are you",
    "My email is test@gmail.com",
    "Phone number is 9876543210",
    "Password@123",
    "I live in Hyderabad"
]

for text in tests:
    print(f"Input: {text}")
    print(validator.validate(text))
    print("-" * 40)
