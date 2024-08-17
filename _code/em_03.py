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
            if letter in string.ascii_uppercase:
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
            # Numbers and special characters are unchanged
            encrypted_message.append(letter)

            # Rotate the rotors
            rotate_next = True
            for rotor in self.rotors:
                if rotate_next:
                    rotate_next = rotor.rotate()

        return ''.join(encrypted_message)

def interactive_enigma():
    print("Welcome to the Interactive Enigma Machine!")

    # Define available rotors in a dictionary
    available_rotors = {
        "1": "SAVJNMITYPOEFWUQZLBGKHXCDR",
        "2": "LKJWSPFIYGMDQOZAERXTHVUBCN",
        "3": "ZBJFAXHUTGVESDYMQIPWKRCLNO",
        "4": "MXTDWJYQFNOVCPSUGIZLREHKAB",
        "5": "BTJZRFLQICKSHEPOAVNXDGUMYW",
        "6": "PBDMILKECVFUAZOSHWGJRYTQNX",
        "7": "XODCYKNJRPSFVMZLATUEQIGWBH",
        "8": "ZRLHTBCYGUOAJWKSQXNMVEPIDF",
        "9": "XSYBPRJWEHAICKUFZVTOLGMNDQ",
        "10": "FSUZWPADGEHCBQNJLTVXORKMYI",
        "11": "FMAXBQDCTRHSIEVYPJNGOWLUZK",
        "12": "KTBNZLUDVCJXIPFMEOHQGYARWS",
        "13": "JWGCULEBSHATZKIQMROFDNYPVX",
        "14": "TXRZPJFLNGSMHBAKOIDUYCVWEQ",
        "15": "BQRFCKXAWMSTDHYZEGPLJUNIOV",
        "16": "RPGDVLTZKYMFIAUJHBQXNOSWCE",
        "17": "UNJTOVMQSEGZDCAHPWBFKRLXIY",
        "18": "OVLCJXHSWZADPYTBIRMEKGFQUN",
        "19": "IHXBFGLVNSJPAYQMWZTKOCUDER",
        "20": "YSTJDROWCKULVBZFQHGAEIPXMN",
        "21": "XNHSKMGOYCWJVQEZATILRPDBUF",
        "22": "WKCIJYZFODBEXUARGNPVLHTQMS",
        "23": "EHXGNCYASPQLFJVTMDWBRZKIUO",
        "24": "FMTBLPIJGQDWKRVESHXOUCZNYA",
        "25": "MUGFTOLIBJWQVYPHKNZRDXACES",
        "26": "YSZUKLNGJITEQDVBPOCAFHRMXW",
        "27": "SNICQZLKMJOXHABRPFYEDUWGVT",
        "28": "OPYEWBQAZGJTXHCLUFNDIKRSVM",
        "29": "WXUZEJGDVSHYFTQILAOMNPCRBK",
        "30": "CDUGTEKXLMIRVQAWPNYFSBOHZJ",
        "31": "IOSNDGKCAFQVXMZEWHBRPTLYJU",
        "32": "JZHMXUFAWTNRDBPLKVGSYOQEIC",
        "33": "FQURHXEGIAODBSZVWKTLYPMCJN",
        "34": "ILRPGETQHUFJWXADBYOCSNZMKV",
        "35": "OXLNEJPCIYGMWQRUTFASHZVDKB",
        "36": "URGSLZMYEFDXIJTPVWAQHKCBON",
        "37": "LGSFIYDHVUKRQAPMOXZNWEBTCJ",
        "38": "HMJWQXCANPSUFOYZLTGRDBEVIK",
        "39": "NLRETQUIDSAPKHZWXGVFJCBMYO",
        "40": "DQMFZWRVNPHOLSBIJTEKCGUXYA",
        "41": "YKQNOTVDWLXMZPSJABCIUEFHGR",
        "42": "IMDUQZKWTGEAXNBLPSJROFCVHY",
        "43": "UZAEFMNYPCTDXGLIRWSQOVKJHB",
        "44": "LTVEFNBGJZSKQHUPDMWICXOAYR",
        "45": "AIGEORXBTPYJZDUWCVMLFNSHQK",
        "46": "SWABFLIJEXDRNVOCTGMHPQZYUK",
        "47": "ODHGALECIMYFQUXTNJWRZPKBSV",
        "48": "CUMHOBTJYXZLAQPFRGDNVIWESK",
        "49": "LPVTZNYSQMOHAIRUKXGEFBDCWJ",
        "50": "GVONKIJLYRMPZXSEWTUFQAHDCB",
        "51": "WYLKCFAJVNMXEDUQTBOGIPZHSR",
        "52": "JCOXUEMLPDBFIWZGANRKSQTHYV",
        "53": "WALEHKBMGYRCVXTDUOSPJZFIQN",
        "54": "ZBSUJALFWIHDQXVPRMYTCKGENO",
        "55": "GNTSAPZLIVYRFCMDWXOQJEKHBU",
        "56": "LICEZJUKBHGAOMNRVTQDFSPXYW",
        "57": "AMRJEXYHUVDGCPZTSLFIBWKNQO",
        "58": "TCJZLWEHIVRKGABSXNDPFQMYUO",
        "59": "BLEFGSPIVOQXJHMDKUNWZYCRTA",
        "60": "ZEYJMLVTKNCSXOAGRIQBFHPWUD",
        "61": "NPRBIFELDKSMHJCWOGUTXAYZVQ",
        "62": "LQPIYEFZTJCRUOGBKXAHDSNVWM",
        "63": "OXQIZBGJHDCVTPRSELFYMKAUWN",
        "64": "YCJITLBHESDPOZWAFVMQGUXKNR",
        "65": "RPFOHELVIYZDWTGCUKBNAJXQMS",
        "66": "PZTYCHKOUISDJFWAXEGLNMQRBV",
        "67": "UASFPGQLZJROKXWBNYVDMEHTIC",
        "68": "CVHYMIJAUDTGPFSEXOZWQRLNBK",
        "69": "TMFWHBRUNKPQYLJAGZEOCDISVX",
        "70": "PZOCKGQRXFMIEJANWLBDSUYVTH",
        "71": "TXUVGASNPJRHYFDQBLMZKCIOWE",
        "72": "GAVNCLIXTPFJRDUKHWOQZMSYEB",
        "73": "OASBXUDGJQRMWCFHNETLYVPKIZ",
        "74": "CAZXNBVLTDREIOYSUWQMGJHKPF",
        "75": "OKZNWDHUMSRBVTIXEPCJAFYQGL",
        "76": "KCBHEUSQMOLRIJTFAZYDWNPXGV",
        "77": "OWGAXKFECPLDMZYTRIJHUNQVBS",
        "78": "MRQYUWJEGONIXKVTBLCDHSAFPZ",
        "79": "WGXYEOLQKFPIJSVRNTBCZDAHMU",
        "80": "MKWAYIXNVJOUDLQRTCEPBGSHZF",
        "81": "YRCLPFZHQBSOEDVKIGWTAUXMJN",
        "82": "AVCYGRIUHBTOMFEPXNSQZKWJDL",
        "83": "JHPVNKZMQBXDOULACWSYGTFERI",
        "84": "CRNUFBLTVEYSJPWXGAOIMDHQKZ",
        "85": "IVMEHTQADNJKPFZUBCSYLGXOWR",
        "86": "ZEWADVMBSFUCGOIHTJXYRPNKLQ",
        "87": "FODBGMUSVPJELYINWKTXCQZHRA",
        "88": "NXGEDVYPQZSHWKRFAMILJTOUCB",
        "89": "MVKYIGHQXNPLEWBSFUOZJTRCDA",
        "90": "KDTCLBERAIPMUONQZHWYFSXGVJ",
        "91": "SIHZWTREJPNQXOALVMDUBKFCGY",
        "92": "XGPBJAHDZQKMNOCVSTYIURLFEW",
        "93": "UEYTWNHRBZGQVLIAJMSCXDPKOF",
        "94": "YAODGRBXLKCWFZHQSVIPUENJMT",
        "95": "CXLGASYVZEJBUTRFHQPDNMKOIW",
        "96": "GWIVYURFHTPDSOCQELMXJZABKN",
        "97": "ATBKDXGPNEJYCISZMWQUROVHFL",
        "98": "NUMRFXDCBJQPYVGTWIAZELKOSH",
        "99": "EKGBUXCSFWVLNMAIDTHZRPYOJQ",
        "100": "VSXUEMYRATDPWHJCLOGZQIFBKN",
    }

    # Maximum number of rotors
    max_rotors = len(available_rotors)
    print(f"Maximum number of rotors available: {max_rotors}")

    # Ask user how many rotors to use
    num_rotors = int(input(f"How many rotors would you like to use? (1-{max_rotors}): "))

    # Ensure the number of rotors is within the valid range
    if not (1 <= num_rotors <= max_rotors):
        print(f"Invalid number of rotors. Please choose between 1 and {max_rotors}.")
        return

    # Choose rotor order
    while True:
        rotor_order_input = input(f"Choose {num_rotors} rotor(s) order (e.g., '1 3 2' within 1-{max_rotors}): ").split()
        if len(rotor_order_input) == num_rotors and all(rotor in available_rotors for rotor in rotor_order_input):
            break
        else:
            print(f"Invalid input. Please choose exactly {num_rotors} rotors from the available options.")

    selected_rotors = [Rotor(available_rotors[rotor]) for rotor in rotor_order_input]

    # User input for rotor positions
    while True:
        rotor_positions_input = input(f"Set rotor positions (e.g., '5 18 3' within 0-25): ").split()
        rotor_positions = [int(pos) for pos in rotor_positions_input]
        if len(rotor_positions) == num_rotors and all(0 <= pos <= 25 for pos in rotor_positions):
            break
        else:
            print(f"Invalid input. Please enter exactly {num_rotors} positions within the range 0-25.")

    for i, rotor in enumerate(selected_rotors):
        rotor.set_position(rotor_positions[i])

    # User input for notch positions
    while True:
        notch_positions_input = input(f"Set notch positions (e.g., '16 4 21' within 0-25): ").split()
        notch_positions = [int(pos) for pos in notch_positions_input]
        if len(notch_positions) == num_rotors and all(0 <= pos <= 25 for pos in notch_positions):
            break
        else:
            print(f"Invalid input. Please enter exactly {num_rotors} notch positions within the range 0-25.")

    for i, rotor in enumerate(selected_rotors):
        rotor.set_notch(notch_positions[i])

    # User input for custom reflector
    use_custom_reflector = input("Would you like to use a custom reflector? (yes/y or no/n): ").strip().lower()

    if use_custom_reflector in ['yes', 'y']:
        while True:
            custom_reflector_input = input("Enter the custom reflector wiring (26 unique uppercase letters): ").strip().upper()
            if len(custom_reflector_input) == 26 and set(custom_reflector_input) == set(string.ascii_uppercase):
                reflector = Reflector(custom_reflector_input)
                break
            else:
                print("Invalid reflector wiring. Please enter exactly 26 unique uppercase letters.")
    else:
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")  # Default reflector

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

    # Create the Enigma machine with selected rotors and reflector
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
