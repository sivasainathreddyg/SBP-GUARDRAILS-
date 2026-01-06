import tempfile
from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings

class SecretValidator:
    def validate(self, text: str) -> dict:

        if not text:
            return {"status": "fail", "type": "empty_input"}

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write(text)
            filename = f.name

        secrets = SecretsCollection()
        with default_settings():
            secrets.scan_file(filename)

        if secrets.json():
            return {"status": "fail", "type": "secret_detected"}

        return {"status": "pass", "type": "no_secret"}
