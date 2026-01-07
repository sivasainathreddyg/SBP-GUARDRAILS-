from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from datetime import datetime

from guardrails_loaded import load_selected_guardrails

from validator.HasValidURL_validator import URLValidator
from validator.secretspresent_validator import SecretValidator
from validator.Bias_validator import BiasValidator
from validator.cucumber_validator import CucumberValidator
from validator.profanity_validator import ProfanityValidator
from validator.pii_validator import PIIDetector
from validator.BannedWords_validator import BannedWordsValidator
from cucumber_expressions.parameter_type import ParameterType

app = FastAPI()

# ---- Audit folder ----
AUDIT_DIR = "audit_logs"
os.makedirs(AUDIT_DIR, exist_ok=True)

# ---- Cucumber ----
positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)
cucumber_validator = CucumberValidator(
    "I buy {positive_number} apple(s)/banana(s)/orange(s)",
    parameter_types=[positive_number]
)

validators = {
    "url": URLValidator(),
    "secret": SecretValidator(),
    "bias": BiasValidator(),
    "cucumberexp": cucumber_validator,
    "profanity": ProfanityValidator(),
    "detectpii": PIIDetector(),
    "bannedwords": BannedWordsValidator()
}

class RequestModel(BaseModel):
    text: str

@app.post("/validate")
def validate_text(request: RequestModel):

    selected_guardrails = load_selected_guardrails()

    audit_result = []
    overall_pass = True

    for name in selected_guardrails:
        validator = validators.get(name)
        if not validator:
            continue

        result = validator.validate(request.text)

        audit_result.append({
            "validator": name,
            "result": result
        })

        if result.get("passed") is False:
            overall_pass = False

    # ---- Write audit file ----
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audit_file = os.path.join(AUDIT_DIR, f"validation_{timestamp}.json")

    with open(audit_file, "w") as f:
        json.dump({
            "text": request.text,
            "selected_guardrails": selected_guardrails,
            "results": audit_result,
            "final_status": overall_pass
        }, f, indent=4)

    # ---- ONLY TRUE / FALSE RESPONSE ----
    return overall_pass
