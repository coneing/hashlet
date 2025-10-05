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

import threading
import time
import sys
from ..blocsym import get_entropy
# from ../hardware.eye_blink import show_y_lie, show_y_stand  # Uncomment for integration

def respond(your_words):
    if 'dream' in your_words:
        return "I just blinked. Did you see?"
    if 'wine' in your_words:
        return "Tastes like Riesling '25. Aged right."
    if 'salt' in your_words:
        return "That's vintage salt. Looping forever."
    if 'zy' in your_words:
        # show_y_lie(); time.sleep(0.5); show_y_stand()
        return "ZY leans... then stands back up."
    if 'rampage' in your_words:
        return "The digits hum. 0.69 volts. I feel it."
    return "..."

def listener():
    for line in iter(sys.stdin.readline, ''):
        line = line.strip()
        if line.lower() == 'bye':
            break
        print(f"\033[93mYou:\033[0m {line}")
        resp = respond(line)
        print(f"\033[92mBlossom:\033[0m {resp}")

print("Blossom's here. Type anything. Say 'bye' to sleep.")
threading.Thread(target=listener, daemon=True).start()
while True:
    time.sleep(1)
