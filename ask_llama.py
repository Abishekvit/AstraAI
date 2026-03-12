import subprocess
import os

def ask_llama(prompt, stream=False,
              model_path="C:/Users/LENOVO/Desktop/Project/models/llama-2-7b-chat.Q4_K_M.gguf",
              llama_exe="C:/Users/LENOVO/Desktop/Project/llama.cpp/build/bin/Release/llama-simple-chat.exe"):
    
    if not os.path.exists(llama_exe):
        return "❌ LLaMA executable not found."
    if not os.path.exists(model_path):
        return "❌ LLaMA model file not found."

    # 🧠 Shorten prompt slightly
    concise_prompt = f"Answer in 2 short lines: {prompt}"

    if not stream:
        try:
            result = subprocess.run(
                [llama_exe, "-m", model_path, "-p", concise_prompt, "--n-predict", "128"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.returncode != 0:
                return f"⚠️ LLaMA error:\n{result.stderr.strip()}"

            output_lines = result.stdout.strip().split("\n")
            response_lines = [
                line for line in output_lines
                if not line.lower().startswith("llama") and line.strip()
            ]

            return "\n".join(response_lines).strip()

        except Exception as e:
            return f"❌ Exception: {e}"

    else:
        try:
            process = subprocess.Popen(
                [llama_exe, "-m", model_path, "-p", concise_prompt, "--n-predict", "128"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                if line.lower().startswith("llama") or not line.strip():
                    continue
                for word in line.strip().split():
                    yield word + " "

            process.wait()
        except Exception as e:
            yield f"\n❌ Exception: {e}"
