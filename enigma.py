# Python basics enigma
# Rotor class assumes input in alphabetical order. Wiring is a string of letters representing the output mapping for each letter.
class Rotor :
    def __init__(self, wiring_forward, wiring_backward, notch, window_letter):
        self.wiring_forward = wiring_forward
        self.wiring_backward = wiring_backward
        self.notch = notch
        self.window_letter = window_letter
    
    def at_notch(self):
        return self.window_letter == self.notch

    def get_backward_wiring(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        backward_wiring = [""] * 26
        for i, letter in enumerate(self.wiring_forward):
            index = ord(letter) - ord('A')
            backward_wiring[index] = alphabet[i]
        return "".join(backward_wiring)


rotor_I = Rotor(
    wiring_forward="EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    wiring_backward="",
    notch="Q",
    window_letter="A"
)

rotor_II = Rotor(
    wiring_forward="AJDKSIRUXBLHWTMCQGZNPYFVOE",
    wiring_backward ="",
    notch="E",
    window_letter="A"
)

rotor_III = Rotor(
    wiring_forward="BDFHJLCPRTXVZNYEIWGAKMUSQO",
    wiring_backward="",
    notch="V",
    window_letter="A"
)

rotor_IV = Rotor(
    wiring_forward="ESOVPZJAYQUIRHXLNFTGKDCMWB",
    wiring_backward="",
    notch="J",
    window_letter="A"
)

rotor_V = Rotor(
    wiring_forward="VZBRGITYUPSDNHLXAWMJQOFECK",
    wiring_backward="",
    notch="Z",
    window_letter="A"
)

rotor_I.wiring_backward = rotor_I.get_backward_wiring()
rotor_II.wiring_backward = rotor_II.get_backward_wiring()
rotor_III.wiring_backward = rotor_III.get_backward_wiring()
rotor_IV.wiring_backward = rotor_IV.get_backward_wiring()
rotor_V.wiring_backward = rotor_V.get_backward_wiring()



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
        output_letter = rotor.wiring_backward[letter_index]
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