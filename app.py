from fastapi import FastAPI
from pydantic import BaseModel
from services.validation_service import ValidationService

app = FastAPI()

validator_service = ValidationService()

class InputText(BaseModel):
    text: str

@app.post("/validate")
def validate_text(input_data: InputText):

    user_text = input_data.text
    results = validator_service.run_all(user_text)

    is_safe = True

    for validator in results.values():
        if validator["matched"] == True:
            is_safe = False
            break

    return {
        "input_text": user_text,
        "is_safe": is_safe,
        "validation_results": results
    }
