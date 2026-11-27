import enigma
import pytest

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------------------------------------------------------------------------
# 1. Independent reference data
# ---------------------------------------------------------------------------
# The published wiring, typed in here separately from enigma.py. Tests should
# not take their expected values from the code they are testing: if enigma.py
# had a typo and the tests read their data from enigma.py, both would agree
# and the typo would never be caught.
REFERENCE_ROTORS = {
    "I":   ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II":  ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV":  ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V":   ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}
ROTOR_NAMES = list(REFERENCE_ROTORS)


# ---------------------------------------------------------------------------
# 2. Fixtures
# ---------------------------------------------------------------------------
# A fixture is a function pytest runs before a test that asks for it by name.
# This one is a "factory fixture": it hands the test a function for building
# rotors, so a test can make as many fresh rotors as it needs, each at its own
# window letter. Nothing is shared between tests, so test order never matters.
#
# When you have several test files that need the same fixture, move it into
# tests/conftest.py. pytest loads that file automatically, and every test file
# in the folder can use its fixtures without importing anything.
@pytest.fixture
def make_rotor():
    def _make(name, window="A"):
        forward, notch = REFERENCE_ROTORS[name]
        return enigma.Rotor(
            wiring_forward=forward,
            wiring_backward=enigma.Rotor(forward, "", "", "A").get_backward_wiring(),
            notch=notch,
            window_letter=window,
        )
    return _make


STEPPING_CASES = [
    pytest.param(("I", "II", "III"), "AAV", ["ABW"], id="right carries middle"),
    pytest.param(("I", "II", "III"), "ADU", ["ADV", "AEW", "BFX"], id="double step"),
    pytest.param(("I", "II", "V"), "AEZ", ["BFA", "BFB"], id="carry to left rotor"),
    pytest.param(("I", "II", "III"), "AAZ", ["AAA"], id="simple step, only carry at notch, not at end of alphabet"),
    pytest.param(("I", "II", "III"), "QAA", ["QAB"], id="Left notch location doesn't matter"),
]

@pytest.mark.parametrize("order, windows, expected", STEPPING_CASES)
def test_stepping(make_rotor, order, windows, expected):
    rotors = [make_rotor(name, window) for name, window in zip(order, windows)]

    right_rotor = rotors[-1]

    middle_rotor = rotors[-2] if len(rotors) > 1 else None

    left_rotor = rotors[-3] if len(rotors) > 2 else None

    for i, exp in enumerate(expected):
        enigma.step_rotors(right_rotor, middle_rotor, left_rotor)
        assert "".join([r.window_letter for r in rotors]) == exp