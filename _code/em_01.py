import string

class Rotor:
    def __init__(self, wiring, ring_setting=0):
        self.wiring = wiring.upper()
        self.ring_setting = ring_setting
        self.position = 0
        self.notch = 0  # Notch will be set by the user

    def set_position(self, position):
        self.position = position % 26

    def set_notch(self, notch):
        self.notch = notch % 26

    def rotate(self):
        self.position = (self.position + 1) % 26
        return self.position == self.notch

    def forward(self, letter):
        index = (string.ascii_uppercase.index(letter) + self.position - self.ring_setting) % 26
        letter = self.wiring[index]
        return string.ascii_uppercase[(string.ascii_uppercase.index(letter) - self.position + self.ring_setting) % 26]

    def backward(self, letter):
        index = (string.ascii_uppercase.index(letter) + self.position - self.ring_setting) % 26
        letter = string.ascii_uppercase[self.wiring.index(string.ascii_uppercase[index])]
        return string.ascii_uppercase[(string.ascii_uppercase.index(letter) - self.position + self.ring_setting) % 26]

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring.upper()

    def reflect(self, letter):
        index = string.ascii_uppercase.index(letter)
        return self.wiring[index]

class Plugboard:
    def __init__(self, wiring=None):
        if wiring is None:
            wiring = {}
        self.wiring = {k.upper(): v.upper() for k, v in wiring.items()}

    def swap(self, letter):
        return self.wiring.get(letter, letter)

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encrypt_decrypt(self, message):
        encrypted_message = []

        for letter in message.upper():
            if letter not in string.ascii_uppercase:
                encrypted_message.append(letter)
                continue

            # Pass through the plugboard
            letter = self.plugboard.swap(letter)

            # Pass through the rotors forward
            for rotor in self.rotors:
                letter = rotor.forward(letter)

            # Pass through the reflector
            letter = self.reflector.reflect(letter)

            # Pass through the rotors backward
            for rotor in reversed(self.rotors):
                letter = rotor.backward(letter)

            # Pass through the plugboard again
            letter = self.plugboard.swap(letter)

            # Append the encrypted letter
            encrypted_message.append(letter)

            # Rotate the rotors
            rotate_next = True
            for rotor in self.rotors:
                if rotate_next:
                    rotate_next = rotor.rotate()

        return ''.join(encrypted_message)

def interactive_enigma():
    print("Welcome to the Interactive Enigma Machine!")

    # Predefined rotors and reflector
    rotor_1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
    rotor_2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE")
    rotor_3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO")
    reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")

    # Choose rotor order
    rotor_order_input = input("Choose rotor order (e.g., '1 3 2'): ")
    rotor_order = [rotor_1, rotor_2, rotor_3]
    rotor_order_dict = {'1': rotor_1, '2': rotor_2, '3': rotor_3}
    selected_rotors = [rotor_order_dict[rotor] for rotor in rotor_order_input.split()]

    # User input for rotor positions
    rotor_positions_input = input("Set rotor positions (e.g., '5 18 3'): ")
    rotor_positions = [int(pos) for pos in rotor_positions_input.split()]
    for i, rotor in enumerate(selected_rotors):
        rotor.set_position(rotor_positions[i])

    # User input for notch positions
    notch_positions_input = input("Set notch positions (e.g., '16 4 21'): ")
    notch_positions = [int(pos) for pos in notch_positions_input.split()]
    for i, rotor in enumerate(selected_rotors):
        rotor.set_notch(notch_positions[i])

    # User input for plugboard settings
    plugboard_pairs = input("Enter plugboard pairs (e.g., 'ab cd ef'): ").upper()
    plugboard_dict = {}
    if plugboard_pairs:
        pairs = plugboard_pairs.split()
        for pair in pairs:
            if len(pair) == 2:
                plugboard_dict[pair[0]] = pair[1]
                plugboard_dict[pair[1]] = pair[0]

    plugboard = Plugboard(plugboard_dict)

    # Create the Enigma machine with selected rotor order
    enigma = EnigmaMachine(selected_rotors, reflector, plugboard)

    # User input for message
    message = input("Enter the message to encrypt/decrypt: ")

    operation = input("Type 'E' to Encrypt or 'D' to Decrypt: ").upper()

    # Encrypt/Decrypt the message
    if operation == 'E':
        result = enigma.encrypt_decrypt(message)
        print(f"Encrypted message: {result}")
    elif operation == 'D':
        result = enigma.encrypt_decrypt(message)
        print(f"Decrypted message: {result}")
    else:
        print("Invalid operation selected.")

    print("Thank you for using the Interactive Enigma Machine!")

# Run the interactive Enigma machine
interactive_enigma()
