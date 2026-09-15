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

WAKE_PHRASE = os.getenv("SYSTEM64_WAKE_PHRASE", "system 64 wake up").lower()
MODEL_PATH = Path(os.getenv("SYSTEM64_VOSK_MODEL", "models/vosk-model-small-en-us"))
SAMPLE_RATE = 16000


class System64WakeWord:
    def __init__(self, on_wake=None):
        self.on_wake = on_wake
        self.running = False
        self.active = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self.running:
            return
        if not MODEL_PATH.exists():
            raise RuntimeError(
                f"Vosk model not found at '{MODEL_PATH}'. "
                "Download a small English Vosk model and place it there."
            )
        self.running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.running = False

    def _listen_loop(self) -> None:
        model = Model(str(MODEL_PATH))
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)
        recognizer.SetWords(False)

        def callback(indata, frames, callback_time, status):
            if status:
                print(f"Microphone status: {status}")
            if not self.running:
                return
            if recognizer.AcceptWaveform(indata):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower().strip()
                if WAKE_PHRASE in text:
                    self._wake()

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
        voice = win32com.client.Dispatch("SAPI.SpVoice")
        voice.Rate = -1
        voice.Volume = 100
        voice.Speak(text)


if __name__ == "__main__":
    listener = System64WakeWord()
    try:
        listener.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
