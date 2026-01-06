import tempfile                                 # used to create a temporary file
from detect_secrets import SecretsCollection    # used to detect the secrets
from detect_secrets.settings import default_settings # default scanning rules (detecting private keys etc)
 
class secret_present:
    def __init__(self, sentence):
        self.sentence = sentence
        self.has_secret = False
        self.check_secret()
 
    def check_secret(self):
        # Write sentence to a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(self.sentence)
            temp_filename = temp_file.name
 
        # Scan using detect_secrets
        secrets = SecretsCollection()
        with default_settings():
            secrets.scan_file(temp_filename)
 
        # Set the result
        self.has_secret = bool(secrets.json())
 
# Input
sentence = input("Enter a prompt: ")
checker = secret_present(sentence)
# print(checker)
# True if secret found, False otherwise
print(checker.has_secret)