import json
import os
import queue
import threading

import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class SpeechEngine:
    def __init__(self, model_path="model/vosk-model-en-us-0.22", sample_rate=16000):
        self.sample_rate = sample_rate
        self.tts_lock = threading.Lock()

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at: {model_path}\n"
                f"Download a model and place it there."
            )

        self.model = Model(model_path)

    def speak(self, text):
        if not text:
            return

        with self.tts_lock:
            engine = pyttsx3.init()
            engine.setProperty("rate", 175)
            engine.say(text)
            engine.runAndWait()
            engine.stop()

    def speak_async(self, text):
        thread = threading.Thread(target=self.speak, args=(text,), daemon=True)
        thread.start()

    def listen(self, duration=6):
        q = queue.Queue()

        def callback(indata, frames, time, status):
            q.put(bytes(indata))

        recognizer = KaldiRecognizer(self.model, self.sample_rate)

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback
        ):
            chunks_needed = max(1, int((self.sample_rate / 8000) * duration))
            for _ in range(chunks_needed):
                data = q.get()
                recognizer.AcceptWaveform(data)

        result = recognizer.FinalResult()
        try:
            text = json.loads(result).get("text", "").strip()
            return text if text else None
        except Exception:
            return None