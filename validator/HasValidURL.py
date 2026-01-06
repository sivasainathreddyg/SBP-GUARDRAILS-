# import re

# class valid_Url:
#     def __init__(self, sentence):
#         self.sentence = sentence
#         self.isValid()

#     def find_match(self):
#         regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")

#         if (self.sentence == None):
#             return False

#         if(re.search(regex, self.sentence)):
#             print("Yes, the given URL is valid.") 
#             return True
#         else:
#             print("No, the given URL is not valid.")
#             return False

# url = input("Enter URL:")
# valid_Url(url)

import re

class URLValidator:
    def __init__(self):
        self.regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" + "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
        
    def find_match(self, text):
        if not text or not isinstance(text, str):
            return False, None

        if re.search(self.regex, text):
            return True, {"type": "url"}

        return False, None
