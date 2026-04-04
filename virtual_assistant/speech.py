import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import threading
import pyttsx3
from faster_whisper import WhisperModel
import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

class SpeechEngine:
    def __init__(self):
        self.model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
        self.tts_lock = threading.Lock()

    def speak(self, text):
        with self.tts_lock:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

    def record_audio(self, duration=4, samplerate=16000):
        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="int16"
        )
        sd.wait()
        return audio, samplerate

    def transcribe(self, audio, samplerate):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, samplerate, audio)

            segments, _ = self.model.transcribe(
                f.name,
                beam_size=5,
                vad_filter=True,          # 🔥 removes silence
                vad_parameters=dict(min_silence_duration_ms=500),
                language="en"             # 🔥 force English (important)
            )

            text = ""
            for segment in segments:
                text += segment.text

        return text.strip().lower()

    def listen(self, duration=3):   # 🔥 shorter = better
        audio, sr = self.record_audio(duration)

        text = self.transcribe(audio, sr)

        if len(text) < 2:
            return ""

        return text

    def listen_wake(self):
        while True:
            try:
                text = self.listen(2)
                if "assistant" in text:
                    return True
            except:
                pass