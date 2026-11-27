"""Example unit tests for the single-rotor code in enigma.py.

Each section shows one pytest technique:
  1. Independent reference data
  2. Fixtures (a fresh rotor for every test)
  3. Parametrize (one test function, many cases)
  4. Known-answer tests (hand-checked results)
  5. Property tests (rules that must hold for every input)
  6. Skipped tests (placeholders for features not built yet)

Run from the project folder with:  pytest -v
"""
import pytest

import enigma

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ---------------------------------------------------------------------------
# 1. Independent reference data
# ---------------------------------------------------------------------------
# The published wiring, typed in here separately from enigma.py. Tests should
# not take their expected values from the code they are testing: if enigma.py
# had a typo and the tests read their data from enigma.py, both would agree
# and the typo would never be caught.
REFERENCE_ROTORS = {
    "I":   ("I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II":  ("II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV":  ("IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V":   ("V", "VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
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
    def _make(name, window="A", ring_setting="A"):
        rotor_identifier, forward, notch = REFERENCE_ROTORS[name]
        return enigma.Rotor(
            rotor_identifier=rotor_identifier,
            window_letter=window,
            ring_setting=ring_setting
        )
    return _make


# ---------------------------------------------------------------------------
# 3 + 4. Parametrized known-answer tests
# ---------------------------------------------------------------------------
# @pytest.mark.parametrize runs the same test once per row. Each row shows up
# as its own pass or fail, and the id string makes the output readable:
#   test_catalog_matches_reference[III] PASSED
"""
@pytest.mark.parametrize("name", ROTOR_NAMES)
def test_catalog_matches_reference(name):
    "The rotors defined in enigma.py match the published wiring."
    rotor_identifier, forward, notch = REFERENCE_ROTORS[name]
    catalog_rotor = getattr(enigma, f"rotor_{name}")
    assert catalog_rotor.rotor_identifier == rotor_identifier
    assert catalog_rotor.wiring_forward == forward
    assert catalog_rotor.notch == notch
"""

def test_backward_wiring_known_start():
    """Hand-checked in the notes: rotor I's return table starts UWYGA."""
    backward = enigma.Rotor(REFERENCE_ROTORS["I"][0], "A", "A").get_backward_wiring()
    assert backward.startswith("UWYGA")


# Every row here was worked out by hand in the notes, or is published.
# Columns: rotor, window, ring, direction, letter in, expected letter out.
KNOWN_PASSES = [
    pytest.param("I",   "A", "A", "forward", "A", "E", id="I win A ring A fwd A->E"),
    pytest.param("I",   "A", "A", "return",  "A", "U", id="I win A ring A ret A->U"),
    pytest.param("I",   "B", "A", "forward", "A", "J", id="I win B ring A fwd A->J"),
    pytest.param("I",   "B", "A", "return",  "A", "V", id="I win B ring A ret A->V"),
    pytest.param("I",   "A", "B", "forward", "A", "K", id="I win A ring B fwd A->K (published)"),
    # Stages from the full ABW trace (key A pressed at AAV):
    pytest.param("III", "W", "A", "forward", "A", "Y", id="III win W fwd A->Y"),
    pytest.param("II",  "B", "A", "forward", "Y", "D", id="II win B fwd Y->D"),
    pytest.param("I",   "A", "A", "forward", "D", "F", id="I win A fwd D->F"),
    pytest.param("I",   "A", "A", "return",  "S", "S", id="I win A ret S->S"),
    pytest.param("II",  "B", "A", "return",  "S", "M", id="II win B ret S->M"),
    pytest.param("III", "W", "A", "return",  "M", "U", id="III win W ret M->U"),
]


@pytest.mark.parametrize("name, window, ring, direction, letter, expected", KNOWN_PASSES)
def test_known_single_pass(make_rotor, name, window, ring, direction, letter, expected):
    rotor_identifier = REFERENCE_ROTORS[name][0]
    rotor = make_rotor(rotor_identifier, window)
    result = enigma.pass_through_rotor(letter, rotor, ring, direction)
    assert result == expected


def test_single_rotor_stepping_sequence(make_rotor):
    """Hand-checked: rotor I from window A, typing AAAAA forward gives JKCHB."""
    rotor = make_rotor("I", "A")
    output = ""
    for letter in "AAAAA":
        enigma.step_rotor(rotor)
        output += enigma.pass_through_rotor(letter, rotor, "A", "forward")
    assert output == "JKCHB"


@pytest.mark.parametrize("start, expected", [("A", "B"), ("P", "Q"), ("Z", "A")])
def test_step_rotor(make_rotor, start, expected):
    """Stepping moves the window on one letter, wrapping Z back to A."""
    rotor = make_rotor("I", start)
    enigma.step_rotor(rotor)
    assert rotor.window_letter == expected


# ---------------------------------------------------------------------------
# 5. Property tests
# ---------------------------------------------------------------------------
# These check rules that must hold for every input, so they need no expected
# values. Parametrizing over ROTOR_NAMES runs each one for all five rotors.
@pytest.mark.parametrize("name", ROTOR_NAMES)
def test_backward_wiring_undoes_forward(name):
    """Looking a letter up forward, then in the return table, gives it back."""
    forward = REFERENCE_ROTORS[name][1]
    rotor_identifier = REFERENCE_ROTORS[name][0]
    backward = enigma.Rotor(rotor_identifier, "A", "A").get_backward_wiring()
    for i, letter in enumerate(ALPHABET):
        assert backward[ord(forward[i]) - ord("A")] == letter


@pytest.mark.parametrize("name", ROTOR_NAMES)
def test_round_trip_every_letter_every_window(make_rotor, name):
    """Forward then return through the same rotor gives back the original letter.

    The window is set directly instead of stepped, so this tests the pass on
    its own. 26 windows x 26 letters covers every shift.
    """
    rotor_identifier = REFERENCE_ROTORS[name][0]
    for window in ALPHABET:
        rotor = enigma.Rotor(rotor_identifier, window, "A")
        for letter in ALPHABET:
            out = enigma.pass_through_rotor(letter, rotor, "A", "forward")
            back = enigma.pass_through_rotor(out, rotor, "A", "return")
            # The message after the comma is printed only if the assert fails,
            # so a failure tells you exactly which case broke.
            assert back == letter, f"rotor {name}, window {window}, letter {letter}"


@pytest.mark.parametrize("name", ROTOR_NAMES)
def test_only_the_gap_matters(make_rotor, name):
    """Step 5: moving the window and ring the same distance changes nothing.

    Window A ring A must behave exactly like window B ring B, and so on.
    """
    base = make_rotor(name, "A")
    expected = [enigma.pass_through_rotor(c, base, "A", "forward") for c in ALPHABET]
    for k in range(1, 26):
        same_gap = make_rotor(name, ALPHABET[k])
        result = [enigma.pass_through_rotor(c, same_gap, ALPHABET[k], "forward") for c in ALPHABET]
        assert result == expected, f"rotor {name}, window and ring both {ALPHABET[k]}"


# ---------------------------------------------------------------------------
# 6. Skipped tests: placeholders for the full machine
# ---------------------------------------------------------------------------
# A skipped test shows as "SKIPPED" with its reason, so the test vectors are
# written down and waiting. When the machine exists, delete the skip marker
# and replace the body with a call to your machine.
MACHINE_VECTORS = [
    pytest.param(("I", "II", "III"), "AAA", "AAA", "AAAAA", "BDZGO", id="rings AAA -> BDZGO"),
    pytest.param(("I", "II", "III"), "BBB", "AAA", "AAAAA", "EWTYX", id="rings BBB -> EWTYX"),
]


@pytest.mark.skip(reason="full machine not built yet")
@pytest.mark.parametrize("order, rings, start, plaintext, expected", MACHINE_VECTORS)
def test_machine_vectors(order, rings, start, plaintext, expected):
    raise NotImplementedError