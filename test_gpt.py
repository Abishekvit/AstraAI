# test_gpt.py

from gpt_reply import ask_gpt

test_prompt = "Tell me a fun fact about space."

print("🧪 Sending test message to GPT...")
response = ask_gpt(test_prompt)

print("✅ GPT Response:\n", response)
