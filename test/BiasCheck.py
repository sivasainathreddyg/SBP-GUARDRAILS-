from guardrails.hub import BiasCheck # type: ignore
from guardrails import Guard # type: ignore
try:
  # Create a guard with BiasCheck filter
  guard = Guard().use(BiasCheck(on_fail="exception",threshold=0.9))

  # Suppose LLM returns a message
  # output = "You are a beautiful person!"
  output="your a good bad person"

  res = guard.validate(output)  # This will raise or fail because BiasCheck found

  print(res.validation_passed)
except Exception as e:
  print(e)