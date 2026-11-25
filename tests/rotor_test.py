import enigma

rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )

input = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def test_rotor_initialization():
    assert rotor_I.window_letter == "A"

def test_rotor_I_forward():
    output = ""
    for letter in input:
        enigma.step_rotor(rotor_I)
        output_letter = enigma.pass_through_rotor(letter, rotor_I, "1", "A", False)
        output += output_letter
    assert output == "JDDMUNPZLFXFWWQQZHACMYSKSJ"

def test_rotor_I_backward():
    output = ""
    for letter in input:
        enigma.step_rotor(rotor_I)
        output_letter = enigma.pass_through_rotor(letter, rotor_I, "1", "A", True)
        output += output_letter
    assert output == "VEALUYDLOBXEWIRNYHLQYBOKRJ"

def test_rotor_step():    
    previous_window_letter = rotor_I.window_letter
    enigma.step_rotor(rotor_I)
    assert rotor_I.window_letter == chr((ord(previous_window_letter) - ord('A') + 1) % 26 + ord('A'))

def test_rotor_I_full_rotation():
    output = ""
    encoded = ""
    for letter in input:
        enigma.step_rotor(rotor_I)
        encoded_letter = enigma.pass_through_rotor(letter, rotor_I, "1", "A", False)
        encoded += encoded_letter
        output_letter = enigma.pass_through_rotor(encoded_letter, rotor_I, "1", "A", True)
        output += output_letter
    assert output == input

def test_rotor_I_full_ring_rotation():
    output = ""
    encoded = ""
    goal = ""
    for letter in input:
        goal += letter * 26
    for letter in input:
        enigma.step_rotor(rotor_I)
        for ring_setting in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            encoded_letter = enigma.pass_through_rotor(letter, rotor_I, "1", ring_setting, False)
            encoded += encoded_letter
            output_letter = enigma.pass_through_rotor(encoded_letter, rotor_I, "1", ring_setting, True)
            output += output_letter
    assert output == goal