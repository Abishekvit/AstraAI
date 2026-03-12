import subprocess
import os
def ask_llama(prompt, model_path="C:/Users/LENOVO/Desktop/Project/models/llama-2-7b-chat.Q4_K_M.gguf"):
    llama_exe = "C:/Users/LENOVO/Desktop/Project/llama.cpp/build/bin/Release/llama-simple-chat.exe"

    try:
        print(f"🧪 Sending prompt to LLaMA: {prompt[:60]}...")

        result = subprocess.run(
            [llama_exe, "-m", model_path],
            input=prompt + "\n",             # Send prompt as stdin
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            return f"⚠️ LLaMA error:\n{result.stderr.strip()}"

        output_lines = result.stdout.strip().split("\n")
        response_lines = [
            line for line in output_lines
            if not line.startswith("llama") and line.strip()
        ]

        return "\n".join(response_lines).strip()

    except Exception as e:
        return f"❌ Exception: {e}"
