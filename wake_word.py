"""Local, muted wake-word listener for System 64.

The microphone is used only for local wake-phrase detection. Audio is not
saved, uploaded, or sent to Ollama. After the wake phrase is detected, the
agent gives a short response through Windows SAPI.

Place a Vosk English model in: models/vosk-model-small-en-us
"""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

try:
    import win32com.client
except ImportError:
    win32com = None

BASE_DIR = Path(__file__).resolve().parent
WAKE_PHRASE = os.getenv("SYSTEM64_WAKE_PHRASE", "system 64 wake up").lower().strip()
MODEL_PATH = Path(os.getenv("SYSTEM64_VOSK_MODEL", str(BASE_DIR / "models" / "vosk-model-small-en-us")))
SAMPLE_RATE = 16000

# Common speech-recognition variants are accepted locally without sending audio anywhere.
WAKE_VARIANTS = {
    WAKE_PHRASE,
    WAKE_PHRASE.replace("system 64", "system sixty four"),
}


class System64WakeWord:
    def __init__(self, on_wake=None):
        self.on_wake = on_wake
        self.running = False
        self.active = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self.running:
            return
        if not MODEL_PATH.exists() or not MODEL_PATH.is_dir():
            raise RuntimeError(
                f"Vosk model not found at '{MODEL_PATH}'. "
                "Extract the English model into models/vosk-model-small-en-us."
            )
        self.running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.running = False

    def _listen_loop(self) -> None:
        try:
            model = Model(str(MODEL_PATH))
            recognizer = KaldiRecognizer(model, SAMPLE_RATE)
            recognizer.SetWords(False)

            def callback(indata, frames, callback_time, status):
                if status:
                    print(f"Microphone status: {status}")
                if not self.running:
                    return
                try:
                    if recognizer.AcceptWaveform(indata):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").lower().strip()
                        if any(phrase in text for phrase in WAKE_VARIANTS):
                            self._wake()
                except Exception as exc:
                    print(f"Wake-word recognition error: {exc}")

            print(f"System 64 wake listener armed for: '{WAKE_PHRASE}'")
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=callback,
            ):
                while self.running:
                    time.sleep(0.2)
        except Exception as exc:
            self.running = False
            print(f"System 64 wake listener stopped: {exc}")

    def _wake(self) -> None:
        if self.active:
            return
        self.active = True
        self.speak("System 64 online. How can I help?")
        if self.on_wake:
            self.on_wake()
        threading.Timer(2.0, self._reset_active).start()

    def _reset_active(self) -> None:
        self.active = False

    @staticmethod
    def speak(text: str) -> None:
        """Speak locally through Windows' installed SAPI voice."""
        if win32com is None:
            print(text)
            return
        try:
            voice = win32com.client.Dispatch("SAPI.SpVoice")
            voice.Rate = -1
            voice.Volume = 100
            voice.Speak(text)
        except Exception as exc:
            print(f"Voice output unavailable: {exc}")
            print(text)


if __name__ == "__main__":
    listener = System64WakeWord()
    try:
        listener.start()
        while listener.running:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
        print("System 64 wake listener stopped.")
