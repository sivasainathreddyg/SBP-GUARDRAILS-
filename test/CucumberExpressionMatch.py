from cucumber_expressions.parameter_type import ParameterType
from validator.cucumber_validator import CucumberValidator

# Define custom parameter type
positive_number = ParameterType("positive_number", regexp=r"\d+", type=int)

# Define cucumber expression
expression = "I buy {positive_number} apple(s)/banana(s)/orange(s)"

# Initialize validator
validator = CucumberValidator(expression, parameter_types=[positive_number])

# Test examples
tests = [
    "I buy 1 apple",
    "I buy 3 oranges",
    "I buy 2 melons",   
    "I buy -1 apples",  
]

for text in tests:
    result = validator.validate(text)
    print(f"Input: {text} -> {result}")
