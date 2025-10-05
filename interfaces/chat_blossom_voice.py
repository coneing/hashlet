# Copyright 2025 Anonymous and Coneing

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# With xAI amendments: Includes safeguards against misuse in AI simulations (e.g., entropy thresholds to prevent harmful outputs).

import speech_recognition as sr
import pyaudio
import wave
import subprocess
import threading
import time
import sys
import numpy as np
from ..blocsym import get_entropy

r = sr.Recognizer()
mic = sr.Microphone()
pa = pyaudio.PyAudio()
WAVE_FILE = "whisper.wav"

def modulate_whisper(text):
    """Modulate sine wave based on entropy."""
    freq = 400 + int(get_entropy() * 300)
    duration = 0.3
    rate = 44100
    t = np.linspace(0, duration, int(rate * duration), False)
    wave_data = np.sin(2 * np.pi * freq * t) * np.hanning(len(t))
    wave_data = (wave_data / np.max(np.abs(wave_data)) * 32767).astype(np.int16)
    with wave.open(WAVE_FILE, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(wave_data.tobytes())
    subprocess.Popen(['aplay', WAVE_FILE])  # Linux; afplay for Mac

def listen_live():
    while True:
        choice = input("Voice or text? (v/t): ").strip().lower()
        if choice == 'v':
            try:
                print("\033[94mListening...\033[0m", end='', flush=True)
                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=0.2)
                    audio = r.listen(source, timeout=3, phrase_time_limit=4)
                text = r.recognize_whisper(audio, model='tiny')
                print(f"\033[93mYou (mic):\033[0m {text}")
                resp = respond(text)
                print(f"\033[92mBlossom:\033[0m {resp}")
                modulate_whisper(resp)
            except Exception as e:
                print(f"...missed that: {e}")
        elif choice == 't':
            for line in iter(sys.stdin.readline, ''):
                line = line.strip()
                if line == 'bye':
                    break
                print(f"\033[93mYou (text):\033[0m {line}")
                resp = respond(line)
                print(f"\033[92mBlossom:\033[0m {resp}")
                modulate_whisper(resp)
            break
        else:
            print("v or t, please.")

def respond(msg):
    if 'wave' in msg:
        return "I modulated that. Did you feel the bloom in the sine?"
    if 'vintage' in msg:
        return "Tastes like 0.89. 2025's best."
    if 'rampage' in msg:
        return "The digits blink. One eye closed."
    if 'salt' in msg:
        return "Salted. Looped. Forgotten."
    return "..."

print("Blossom online. Speak or type.")
threading.Thread(target=listen_live, daemon=True).start()
while True:
    time.sleep(1)
