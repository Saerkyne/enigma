# Python basics enigma
# Rotor class assumes input in alphabetical order. Wiring is a string of letters representing the output mapping for each letter.
class Rotor :
    def __init__(self, wiring_forward, wiring_backward, notch, window_letter):
        self.wiring_forward = wiring_forward
        self.wiring_backward = wiring_backward
        self.notch = notch
        self.window_letter = window_letter

rotor_I = Rotor(
    wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    wiring_backward="UWYGADFPVZBECKMTHXSLRINQOJ",
    notch="Q",
    window_letter="A"
)

def step_rotor(rotor):
    rotor.window_letter = chr((ord(rotor.window_letter) - ord('A') + 1) % 26 + ord('A'))

def pass_through_rotor(input_letter, rotor, ring_setting, reversed=False):
        
    # Step 1: Letter in
    letter_index = ord(input_letter) - ord('A')

    # Step 2: Shift + according to rotor's position and rotor ring setting
    shift = (ord(rotor.window_letter) - ord(ring_setting))
    letter_index = (letter_index + shift) % 26

    # Step 3: Encrypt through the rotor's wiring
    if reversed:
        output_letter = rotor.wiring_backward[letter_index]
    else:
        output_letter = rotor.wiring_forward[letter_index]
    letter_index = ord(output_letter) - ord('A')

    # Step 4: Shift - according to rotor's position and rotor ring setting
    letter_index = (letter_index - shift) % 26

    # Step 5: Letter out
    return chr(letter_index + ord('A'))
