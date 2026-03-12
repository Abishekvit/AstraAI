from llama_reply import ask_llama

prompt = "Explain why the sky is blue."
print("🧪 Sending prompt to LLaMA...\n")
response = ask_llama(prompt)
print("✅ LLaMA Response:\n", response)
