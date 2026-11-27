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

def get_backward_wiring(forward_wiring):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    backward_wiring = [""] * 26
    for i, letter in enumerate(forward_wiring):
        index = ord(letter) - ord('A')
        backward_wiring[index] = alphabet[i]
    return "".join(backward_wiring)

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

rotor_I.wiring_backward = get_backward_wiring(rotor_I.wiring_forward)
rotor_II.wiring_backward = get_backward_wiring(rotor_II.wiring_forward)
rotor_III.wiring_backward = get_backward_wiring(rotor_III.wiring_forward)
rotor_IV.wiring_backward = get_backward_wiring(rotor_IV.wiring_forward)
rotor_V.wiring_backward = get_backward_wiring(rotor_V.wiring_forward)

def step_rotors(right, middle, left):
    right_notched = right.at_notch() if right else False
    middle_notched = middle.at_notch() if middle else False
    
    
    # Always advance the right rotor
    if right:
        step_rotor(right)
        print(f"Right rotor stepped from {chr((ord(right.window_letter) - ord('A') - 1) % 26 + ord('A'))} to {right.window_letter}")
    
    # If the right rotor was at its notch before rotating, step the middle rotor
    if middle and right_notched:
        step_rotor(middle)

    # If the middle rotor was at its notch before rotating, step the left rotor
    if left and middle_notched:
        step_rotor(left)
        # This also steps the middle rotor again due to the double-stepping mechanism
        step_rotor(middle)
    else:
        pass
    
    print(f"Rotor positions: Right={right.window_letter if right else 'N/A'}, Middle={middle.window_letter if middle else 'N/A'}, Left={left.window_letter if left else 'N/A'}")