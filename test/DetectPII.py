import re
from guardrails import Guard
from guardrails.hub import DetectPII
 
password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{6,}$"
 
guard = Guard().use(
    DetectPII(on_fail="exception")
)
 
def is_sensitive(text):
    """
    Returns True if the input contains PII or matches password regex.
    Returns False if input is safe.
    """
    if re.fullmatch(password_pattern, text):
        return True
 
    try:
        guard.validate(text)
        return False  
    except Exception:
        return True  
       
text = input("Enter input: ")
print(is_sensitive(text))