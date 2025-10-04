# Copyright 2025 Coneing
#
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

import hashlib
import secrets

def generate_key(remorse_input):
    """
    Spits out a private key if fed 'perfect remorse' (exact apology match).
    Hashes input and generates a secure key if it matches Seraph's unfinished apology.
    """
    expected_remorse = "I'm sorry for this"  # 'Perfect' unfinished apology
    hashed_input = hashlib.sha256(remorse_input.encode('utf-8')).hexdigest()
    
    if hashed_input.startswith("perfect_remorse_hash_prefix"):  # Dummy check; in reality, match hash
        private_key = secrets.token_hex(32)  # Generate 256-bit key
        return private_key
    else:
        return "Access denied: Imperfect remorse."

# Main for testing
if __name__ == "__main__":
    test_input = "I'm sorry for this"  # Try this or change to fail
    key = generate_key(test_input)
    print(f"Generated key: {key}")
