# Copyright (C) 2025 Anonymous, Coneing
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import secrets

def generate_key(remorse_input, veto=False):
    """
    Generates key on perfect remorse match; unlocks sim elements.
    Post-fork: Adds TACSI veto for unethical inputs.
    Returns key or denial.
    """
    if veto:
        return "Veto: not okay"
    
    expected = "I'm sorry for this"
    if remorse_input == expected:
        return secrets.token_hex(32)
    return "Imperfect remorse."

# Main for testing
if __name__ == "__main__":
    key = generate_key("I'm sorry for this")
    print(f"Key: {key}")
