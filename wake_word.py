"""Always-listening, muted wake-word service for System 64.

The microphone is used only to detect the configured wake phrase locally.
No audio is saved or sent to Ollama. After the phrase is detected, this module
can notify the desktop UI and speak a short response with Windows SAPI.
"""

from __future__ import annotations

import os
import threading
import time

WAKE_PHRASE = os.getenv("SYSTEM64_WAKE_PHRASE", "system 64 wake up").lower()

try:
    import speech_recognition as sr
except ImportError:  # Optional until dependencies are installed.
    sr = None

try:
    import win32com.client
except ImportError:  # Optional until pywin32 is installed.
    win32com = None


class System64WakeWord:
    def __init__(self, on_wake=None):
        self.on_wake = on_wake
        self.running = False
        self.active = False
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if sr is None:
            raise RuntimeError("SpeechRecognition is not installed. Run: pip install SpeechRecognition PyAudio pywin32")
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self.running = False

    def _listen_loop(self) -> None:
        recognizer = sr.Recognizer()
        recognizer.dynamic_energy_threshold = True
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

        while self.running:
            try:
                with microphone as source:
                    # Short local listening windows keep the agent responsive while muted.
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower().strip()
                if WAKE_PHRASE in text:
                    self.active = True
                    self.speak("System 64 online. How can I help?")
                    if self.on_wake:
                        self.on_wake()
                    time.sleep(1)
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except Exception as exc:
                print(f"Wake-word listener paused: {exc}")
                time.sleep(2)

    @staticmethod
    def speak(text: str) -> None:
        """Speak locally through Windows' installed SAPI voice."""
        if win32com is None:
            print(text)
            return
        voice = win32com.client.Dispatch("SAPI.SpVoice")
        voice.Speak(text)


if __name__ == "__main__":
    print(f"System 64 wake listener armed for: '{WAKE_PHRASE}'")
    listener = System64WakeWord()
    listener.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
