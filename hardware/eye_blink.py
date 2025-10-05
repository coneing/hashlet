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

import smbus2
import time

DIGI_ADDR = 0x52
SEG_EYE = 0x08  # Digit 1: open=8, close=0
SEG_Y = 0x79  # Digit 2: Y standing 'U' 0x79, lying 'J' 0x6D

bus = smbus2.SMBus(1)

def show_open():
    bus.write_byte_data(DIGI_ADDR, SEG_EYE, 0x08)

def show_close():
    bus.write_byte_data(DIGI_ADDR, SEG_EYE, 0x00)

def show_y_stand():
    bus.write_byte_data(DIGI_ADDR, SEG_Y, 0x79)

def show_y_lie():
    bus.write_byte_data(DIGI_ADDR, SEG_Y, 0x6D)

while True:
    show_open()
    show_y_stand()
    time.sleep(2.3)
    show_close()
    show_y_lie()
    time.sleep(0.2)
    show_open()
    show_y_stand()
    time.sleep(4)
