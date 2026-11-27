# Python basics enigma
# Rotor class assumes input in alphabetical order. Wiring is a string of letters representing the output mapping for each letter.
class Rotor :
    def __init__(self, rotor_identifier, window_letter, ring_setting):
        self.window_letter = window_letter
        self.ring_setting = ring_setting
        if rotor_identifier == "I":
            self.wiring_forward = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            self.notch = "Q"
        elif rotor_identifier == "II":
            self.wiring_forward = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            self.notch = "E"
        elif rotor_identifier == "III":
            self.wiring_forward = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            self.notch = "V"
        elif rotor_identifier == "IV":
            self.wiring_forward = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            self.notch = "J"
        elif rotor_identifier == "V":
            self.wiring_forward = "VZBRGITYUPSDNHLXAWMJQOFECK"
            self.notch = "Z"
    
    def at_notch(self):
        return self.window_letter == self.notch

    def get_backward_wiring(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        backward_wiring = [""] * 26
        for i, letter in enumerate(self.wiring_forward):
            index = ord(letter) - ord('A')
            backward_wiring[index] = alphabet[i]
        return "".join(backward_wiring)

encrypt_rotor_I = Rotor("I", "A", "A")
encrypt_rotor_II = Rotor("II", "A", "A")
encrypt_rotor_III = Rotor("III", "A", "A")
encrypt_rotor_IV = Rotor("IV", "A", "A")
encrypt_rotor_V = Rotor("V", "A", "A")

decrypt_rotor_I = Rotor("I", "A", "A")
decrypt_rotor_II = Rotor("II", "A", "A")
decrypt_rotor_III = Rotor("III", "A", "A")
decrypt_rotor_IV = Rotor("IV", "A", "A")
decrypt_rotor_V = Rotor("V", "A", "A")

def step_rotor(rotor):
    rotor.window_letter = chr((ord(rotor.window_letter) - ord('A') + 1) % 26 + ord('A'))
    
def pass_through_rotor(input_letter, rotor, ring_setting, direction):
        
    # Step 1: Letter in
    letter_index = ord(input_letter) - ord('A')

    # Step 2: Shift + according to rotor's position and rotor ring setting
    shift = (ord(rotor.window_letter) - ord(ring_setting))
    letter_index = (letter_index + shift) % 26

    # Step 3: Encrypt through the rotor's wiring
    if direction == "return":
        output_letter = rotor.get_backward_wiring()[letter_index]
    elif direction == "forward":
        output_letter = rotor.wiring_forward[letter_index]
    letter_index = ord(output_letter) - ord('A')

    # Step 4: Shift - according to rotor's position and rotor ring setting
    letter_index = (letter_index - shift) % 26

    # Step 5: Letter out
    return chr(letter_index + ord('A'))

def step_rotors(right, middle, left):
    right_notched = right.at_notch() if right else False
    middle_notched = middle.at_notch() if middle else False
    middle_step = False
    left_step = False
    
    if middle and right_notched:
        middle_step = True
    if left and middle_notched:
        left_step = True
    if middle and left and middle_notched:
        middle_step = True
        left_step = True
    
    # Always advance the right rotor
    if right:
        step_rotor(right)
    if middle_step:
        step_rotor(middle)
    if left_step:
        step_rotor(left)