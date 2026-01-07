from fastapi import FastAPI
from pydantic import BaseModel
from executor import execute_validators

app=FastAPI()


# class RequestModel(BaseModel):
#     text:str
#     validator:str
    
# @app.post("/validate")
# def validate_text(request: RequestModel):

#     validator = validators.get(request.validator)

#     if not validator:
#         return {
#             "status": "error",
#             "message": "Validator not supported"
#         }

#     return validator.validate(request.text)

class TextRequest(BaseModel):
    text: str


@app.post("/validate")
def validate_text(request: TextRequest):
    return execute_validators(request.text)