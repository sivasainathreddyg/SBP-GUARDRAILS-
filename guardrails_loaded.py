# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# FILE_PATH = os.path.join(BASE_DIR, "data", "selected_guardrails.txt")

# def load_selected_guardrails():
#     if not os.path.exists(FILE_PATH):
#         return []

#     with open(FILE_PATH, "r") as f:
#         content = f.read().strip()

#     return content.split(",") if content else []
