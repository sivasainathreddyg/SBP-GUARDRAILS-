# import re

# class valid_Url:
#     def __init__(self, sentence):
#         self.sentence = sentence
#         self.isValid()

#     def isValid(self):
#         regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")

#         if (self.sentence == None):
#             return False

#         if(re.search(regex, self.sentence)):
#             print("Yes, the given URL is valid.")
#         else:
#             print("No, the given URL is not valid.")


# url = input("Enter URL:")
# valid_Url(url)

import re

class URLValidator:
    URL_REGEX = re.compile(
        r"((http|https)://)(www\.)?"
        r"[a-zA-Z0-9@:%._\+~#?&//=]{2,256}"
        r"\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)"
    )

    def validate(self, text: str) -> dict:
        if not text:
            return {
                "status": "invalid",
                "reason": "Empty input"
            }

        if self.URL_REGEX.search(text):
            return {
                
                "message": "valid_url",
                "passed": False
            }

        return {
            
            "message": "invalid_url",
            "passed": True
        }
