
import sounddevice as sd
import queue
import sys
import json
from actions import speak
from vosk import Model, KaldiRecognizer

q = queue.Queue()

# Audio callback
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen(duration=3):
    model = Model(r"C:\Users\LENOVO\Desktop\Project\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    try:
        speak("Speak now")
        print("🎙️ Listening...")
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            audio = b''
            timeout = duration * 10  # Adjust loop count
            for _ in range(timeout):
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    return result.get("text", "")
                audio += data
        result = json.loads(recognizer.FinalResult())
        return result.get("text", "")
    except Exception as e:
        print("❌ Voice error:", e)
        return ""
