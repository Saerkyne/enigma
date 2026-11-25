import enigma



input_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def test_rotor_initialization():
    rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )
    assert rotor_I.window_letter == "A"

def test_rotor_I_forward():
    rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )
    output = ""
    for letter in input_string:
        enigma.step_rotor(rotor_I)
        output_letter = enigma.pass_through_rotor(letter, rotor_I, "A", False)
        output += output_letter
    assert output == "JDDMUNPZLFXFWWQQZHACMYSKSJ"

def test_rotor_I_backward():
    rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )
    output = ""
    for letter in input_string:
        enigma.step_rotor(rotor_I)
        output_letter = enigma.pass_through_rotor(letter, rotor_I, "A", True)
        output += output_letter
    assert output == "VEALUYDLOBXEWIRNYHLQYBOKRJ"

def test_rotor_step():    
    rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )
    previous_window_letter = rotor_I.window_letter
    enigma.step_rotor(rotor_I)
    assert rotor_I.window_letter == chr((ord(previous_window_letter) - ord('A') + 1) % 26 + ord('A'))

def test_rotor_I_full_ring_rotation():
    rotor_I = enigma.Rotor(
        wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
        notch="Q",
        window_letter="A"
    )
    output = ""
    encoded = ""
    goal = ""
    for letter in input_string:
        goal += letter * 26
    for letter in input_string:
        enigma.step_rotor(rotor_I)
        for ring_setting in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            encoded_letter = enigma.pass_through_rotor(letter, rotor_I, ring_setting, False)
            encoded += encoded_letter
            output_letter = enigma.pass_through_rotor(encoded_letter, rotor_I, ring_setting, True)
            output += output_letter
    assert output == goal