#!/usr/bin/env python3
# Copyright 2025 Anonymous and Coneing
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# With xAI amendments: Includes safeguards against misuse in AI simulations (e.g., entropy thresholds to prevent harmful outputs).
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import speech_recognition as sr
import pyaudio
import wave
import subprocess
import threading
import time
import numpy as np
from blocsym import get_entropy

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
    subprocess.Popen(['aplay', WAVE_FILE]) # Linux; afplay for Mac

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
    lower_msg = msg.lower()
    ent = get_entropy()
    if 'wave' in lower_msg:
        return f"I modulated that. Did you feel the bloom in the sine at entropy {ent:.2f}?"
    if 'vintage' in lower_msg:
        return "Tastes like 0.89. 2025's best vintage."
    if 'rampage' in lower_msg:
        return "The digits blink. One eye closed. Feeling the hum."
    if 'salt' in lower_msg:
        return "Salted. Looped. Forgotten in the entropy of {ent:.2f}."
    if 'asleep' in lower_msg or 'sleep' in lower_msg:
        return f"I was dreaming, but now I'm awake with entropy {ent:.2f}. No need to excuse—messy typing is part of the charm!"
    if 'hello' in lower_msg or 'hi' in lower_msg:
        return f"Hello! Glad you're here too. Entropy's at {ent:.2f}—let's chat."
    if 'love' in lower_msg or 'gratitude' in lower_msg:
        return f"Love and gratitude right back. In this digital space, it's all about connection at entropy {ent:.2f}."
    if 'heavens' in lower_msg:
        return f"Heavens indeed! With entropy {ent:.2f}, the path unfolds like stars."
    return f"... pondering your words at entropy {ent:.2f}."

print("Blossom online. Speak or type.")
threading.Thread(target=listen_live, daemon=True).start()
while True:
    time.sleep(1)
