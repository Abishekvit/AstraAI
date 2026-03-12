from voice import listen
from ask_llama_streaming import ask_llama

def main():
    print("🧠 Speak now:")
    query = listen()
    if not query:
        print("❌ No voice input detected.")
        return

    print(f"🎤 You asked: {query}")
    response = ask_llama(query, n_predict=32)
    print("✅ LLaMA Response:\n", response)

if __name__ == "__main__":
    main()
