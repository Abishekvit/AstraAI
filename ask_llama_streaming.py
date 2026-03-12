import subprocess

def ask_llama(prompt, n_predict=16, model_path="C:/Users/LENOVO/Desktop/Project/models/llama-2-7b-chat.Q4_K_M.gguf"):
    llama_exe = "C:/Users/LENOVO/Desktop/Project/llama.cpp/build/bin/Release/llama-simple-chat.exe"
    concise_prompt = f"{prompt.strip()} (Answer in one short line only)"

    try:
        result = subprocess.run(
            [
                llama_exe,
                "-m", model_path,
                "-p", concise_prompt,
                "-n", str(n_predict)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("⚠️ stderr:\n", result.stderr.strip())  # Debug
        print("⚠️ stdout:\n", result.stdout.strip())  # Debug

        if result.returncode != 0 or "example usage:" in result.stdout.lower():
            return "❌ LLaMA Error: Model failed to execute properly."

        output_lines = result.stdout.strip().split("\n")
        response_lines = [line for line in output_lines if not line.startswith("llama")]
        return "\n".join(response_lines).strip()

    except Exception as e:
        return f"❌ Exception: {e}"
