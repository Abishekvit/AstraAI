import subprocess

def ask_llama(prompt, model_path="models/llama-2-7b-chat.Q4_K_M.gguf"):
    llama_exe = "build/bin/Release/llama-simple-chat.exe"  # Update path if needed

    command = [
        llama_exe,
        "-m", model_path,
        "-p", prompt,
        "--n-predict", "200"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"❌ Error: {e}"
