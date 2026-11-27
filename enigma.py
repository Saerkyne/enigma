# Python basics enigma
# Rotor class assumes input in alphabetical order. Wiring is a string of letters representing the output mapping for each letter.
class Rotor :
    def __init__(self, rotor_identifier, window_letter, ring_setting):
        self.window_letter = window_letter
        self.ring_setting = ring_setting
        if rotor_identifier == "I":
            self.wiring_forward = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            self.notch = "Q"
            self.wiring_backward = self.set_backward_wiring()
        elif rotor_identifier == "II":
            self.wiring_forward = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            self.notch = "E"
            self.wiring_backward = self.set_backward_wiring()
        elif rotor_identifier == "III":
            self.wiring_forward = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            self.notch = "V"
            self.wiring_backward = self.set_backward_wiring()
        elif rotor_identifier == "IV":
            self.wiring_forward = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            self.notch = "J"
            self.wiring_backward = self.set_backward_wiring()
        elif rotor_identifier == "V":
            self.wiring_forward = "VZBRGITYUPSDNHLXAWMJQOFECK"
            self.notch = "Z"
            self.wiring_backward = self.set_backward_wiring()
    
    def at_notch(self):
        return self.window_letter == self.notch

    def set_backward_wiring(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        backward_wiring = [""] * 26
        for i, letter in enumerate(self.wiring_forward):
            index = ord(letter) - ord('A')
            backward_wiring[index] = alphabet[i]
        return "".join(backward_wiring)

class Reflector:
    def __init__(self, reflector_identifier):
        if reflector_identifier == "A":
            self.wiring = "EJMZALYXVBWFCRQUONTSPIKHGD"
        elif reflector_identifier == "B":
            self.wiring = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        elif reflector_identifier == "C":
            self.wiring = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

    def reflect(self, input_letter):
        index = ord(input_letter) - ord('A')
        return self.wiring[index]

class Plugboard:
    def __init__(self):
        self.pair_one = None
        self.pair_two = None
        self.pair_three = None
        self.pair_four = None
        self.pair_five = None
        self.pair_six = None
        self.pair_seven = None
        self.pair_eight = None
        self.pair_nine = None
        self.pair_ten = None

    def configure(self, mappings):
        pairs = [
            "pair_one", "pair_two", "pair_three", "pair_four", "pair_five",
            "pair_six", "pair_seven", "pair_eight", "pair_nine", "pair_ten"
        ]
        for i, (a, b) in enumerate(mappings):
            if i < 10:
                setattr(self, pairs[i], (a, b))
    
    def encode(self, input_letter):
        for pair in [
            self.pair_one, self.pair_two, self.pair_three, self.pair_four, self.pair_five,
            self.pair_six, self.pair_seven, self.pair_eight, self.pair_nine, self.pair_ten
        ]:
            if pair and input_letter in pair:
                return pair[1] if input_letter == pair[0] else pair[0]
        return input_letter

ROTOR_NAMES = ["I", "II", "III", "IV", "V"]
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def step_rotor(rotor):
    rotor.window_letter = chr((ord(rotor.window_letter) - ord('A') + 1) % 26 + ord('A'))
    
def pass_through_rotor(input_letter, rotor, direction):
        
    # Step 1: Letter in
    letter_index = ord(input_letter) - ord('A')

    # Step 2: Shift + according to rotor's position and rotor ring setting
    shift = (ord(rotor.window_letter) - ord(rotor.ring_setting))
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

def pass_through_reflector(input_letter, reflector):
    return reflector.reflect(input_letter)

def pass_through_plugboard(input_letter, plugboard):
    if plugboard is None:
        return input_letter
    
    return plugboard.encode(input_letter)


def encrypt(rotor_choice, rotor_windows, rotor_ring_settings, plugboard_settings, message):
    encrypt_plugboard = Plugboard()
    encrypt_plugboard.configure([tuple(setting) for setting in plugboard_settings])

    encrypt_left_rotor = Rotor(rotor_choice[0], rotor_windows[0], rotor_ring_settings[0])
    encrypt_middle_rotor = Rotor(rotor_choice[1], rotor_windows[1], rotor_ring_settings[1])
    encrypt_right_rotor = Rotor(rotor_choice[2], rotor_windows[2], rotor_ring_settings[2])

    encrypt_reflector = Reflector("B")

    ciphertext = ""
    for letter in message.upper():
        if letter == " ":
            ciphertext += " "
            continue
        if letter not in ALPHABET:
            print(f"Invalid character in message: {letter}. Only letters A-Z are allowed.")
            raise ValueError(f"Invalid character in message: {letter}. Only letters A-Z are allowed.")
        letter = pass_through_plugboard(letter, encrypt_plugboard)
        step_rotors(encrypt_right_rotor, encrypt_middle_rotor, encrypt_left_rotor)
        letter = pass_through_rotor(letter, encrypt_right_rotor, "forward")
        letter = pass_through_rotor(letter, encrypt_middle_rotor, "forward")
        letter = pass_through_rotor(letter, encrypt_left_rotor, "forward")
        letter = pass_through_reflector(letter, encrypt_reflector)
        letter = pass_through_rotor(letter, encrypt_left_rotor, "return")
        letter = pass_through_rotor(letter, encrypt_middle_rotor, "return")
        letter = pass_through_rotor(letter, encrypt_right_rotor, "return")
        letter = pass_through_plugboard(letter, encrypt_plugboard)
        ciphertext += letter

    return ciphertext




def user_interaction():


    # Get encryption settings from user
    print("Enter encryption settings:")
    rotor_choice = input("Choose rotor order (e.g., I II III): ").split()
    if len(rotor_choice) != 3:
        print("Invalid rotor choice. You must choose exactly 3 rotors.")
        exit()
    rotor_choice = [rotor.upper() for rotor in rotor_choice]
    if any(rotor not in ROTOR_NAMES for rotor in rotor_choice):
        print(f"Invalid rotor choice. Valid options are: {', '.join(ROTOR_NAMES)}")
        exit()
    # Validate rotor choice against available rotor names
    used_rotors = set()
    for rotor in rotor_choice:
        if rotor in used_rotors:
            print(f"Invalid rotor choice. Rotor {rotor} is used more than once.")
            exit()
        used_rotors.add(rotor)
    
    rotor_windows = input("Enter rotor starting window letters (e.g., A B C): ").split()
    if len(rotor_windows) != 3:
        print("Invalid rotor windows. You must enter exactly 3 letters.")
        exit()
    rotor_windows = [w.upper() for w in rotor_windows]
    if any(w not in ALPHABET for w in rotor_windows):
        print(f"Invalid rotor windows. Valid options are: {', '.join(ALPHABET)}")
        exit()
    
    rotor_ring_settings = input("Enter rotor ring settings (e.g., A B C): ").split()
    if len(rotor_ring_settings) != 3:
        print("Invalid rotor ring settings. You must enter exactly 3 letters.")
        exit()
    rotor_ring_settings = [r.upper() for r in rotor_ring_settings]
    if any(r not in ALPHABET for r in rotor_ring_settings):
        print(f"Invalid rotor ring settings. Valid options are: {', '.join(ALPHABET)}")
        exit()

    plugboard_settings = input("Enter plugboard settings, 10 pairs spaced. If none, leave empty: ").split()
    if plugboard_settings and len(plugboard_settings) != 10:
        print("Invalid plugboard settings. You must enter exactly 10 pairs.")
        exit()
    plugboard_settings = [p.upper() for p in plugboard_settings]
    if any(len(p) != 2 or any(c not in ALPHABET for c in p) for p in plugboard_settings):
        print(f"Invalid plugboard settings. Each pair must consist of two letters A-Z.")
        exit()
    # Check that each letter is only used once in the plugboard
    used_letters = set()
    for pair in plugboard_settings:
        for letter in pair:
            if letter in used_letters:
                print(f"Invalid plugboard settings. Letter {letter} is used more than once.")
                exit()
            used_letters.add(letter)

    print("Enter message to encrypt: ")
    message = input()

    ciphertext = encrypt(rotor_choice, rotor_windows, rotor_ring_settings, plugboard_settings, message)
    

    print("Encrypted message: ", ciphertext)

if __name__ == "__main__":
    user_interaction()