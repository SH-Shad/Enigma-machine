import sys
import string
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QSpinBox, QTabWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt  # Import Qt for alignment options

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

class EnigmaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Enigma Machine')

        # Set the window size
        self.resize(600, 600)  # Width, Height

        # Create a tab widget
        self.tabs = QTabWidget()
        
        # Create the main tab and the about tab
        self.main_tab = QWidget()
        self.about_tab = QWidget()
        
        self.tabs.addTab(self.main_tab, "Enigma Machine")
        self.tabs.addTab(self.about_tab, "About")

        # Layout for the main tab
        main_layout = QVBoxLayout()

        # Define a font with a larger size
        font = QFont("Arial", 12)

        # Number of Rotors Selection
        self.rotor_count_spinbox = QSpinBox()
        self.rotor_count_spinbox.setRange(1, 100)  # Updated to allow up to 100 rotors
        self.rotor_count_spinbox.setValue(3)
        self.rotor_count_spinbox.setFont(font)

        rotor_count_layout = QHBoxLayout()
        rotor_count_label = QLabel('Number of Rotors:')
        rotor_count_label.setFont(font)
        rotor_count_layout.addWidget(rotor_count_label)
        rotor_count_layout.addWidget(self.rotor_count_spinbox)
        main_layout.addLayout(rotor_count_layout)

        # Rotor order input
        order_layout = QHBoxLayout()
        order_label = QLabel('Rotor Order:')
        order_label.setFont(font)
        self.order_input = QLineEdit()
        self.order_input.setFont(font)
        self.order_input.setPlaceholderText("e.g., '1 10 100' within 1-100")  # Placeholder text added
        order_layout.addWidget(order_label)
        order_layout.addWidget(self.order_input)
        main_layout.addLayout(order_layout)

        # Rotor positions input
        position_layout = QHBoxLayout()
        position_label = QLabel('Rotor Positions:')
        position_label.setFont(font)
        self.position_input = QLineEdit()
        self.position_input.setFont(font)
        self.position_input.setPlaceholderText("e.g., '5 18 3' within 0-25")  # Placeholder text added
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_input)
        main_layout.addLayout(position_layout)

        # Rotor notches input
        notch_layout = QHBoxLayout()
        notch_label = QLabel('Notch Positions:')
        notch_label.setFont(font)
        self.notch_input = QLineEdit()
        self.notch_input.setFont(font)
        self.notch_input.setPlaceholderText("e.g., '16 4 21' within 0-25")  # Placeholder text added
        notch_layout.addWidget(notch_label)
        notch_layout.addWidget(self.notch_input)
        main_layout.addLayout(notch_layout)

        # Plugboard settings
        plugboard_layout = QHBoxLayout()
        plugboard_label = QLabel('Plugboard Settings:')
        plugboard_label.setFont(font)
        self.plugboard_input = QLineEdit()
        self.plugboard_input.setFont(font)
        self.plugboard_input.setPlaceholderText("e.g., AB CD EF..")  # Placeholder text added
        plugboard_layout.addWidget(plugboard_label)
        plugboard_layout.addWidget(self.plugboard_input)
        main_layout.addLayout(plugboard_layout)

        # Message input
        message_layout = QVBoxLayout()
        message_label = QLabel('Message:')
        message_label.setFont(font)
        self.message_input = QTextEdit()
        self.message_input.setFont(font)
        message_layout.addWidget(message_label)
        message_layout.addWidget(self.message_input)
        main_layout.addLayout(message_layout)

        # Buttons for encryption and decryption
        button_layout = QHBoxLayout()
        self.encrypt_button = QPushButton('Encrypt')
        self.encrypt_button.setFont(font)
        self.encrypt_button.setFixedHeight(40)
        self.encrypt_button.clicked.connect(self.encrypt_message)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton('Decrypt')
        self.decrypt_button.setFont(font)
        self.decrypt_button.setFixedHeight(40)
        self.decrypt_button.clicked.connect(self.decrypt_message)
        button_layout.addWidget(self.decrypt_button)

        main_layout.addLayout(button_layout)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setFont(font)
        self.output_area.setReadOnly(True)
        main_layout.addWidget(self.output_area)

        self.main_tab.setLayout(main_layout)

        # About Tab Content
        about_layout = QVBoxLayout()
        about_label = QLabel("Enigma Machine\nVersion 1.0\n\nCreated by: Your Name\n\nThis application simulates the functionality of the Enigma Machine, a cipher device used by the Germans during World War II.")
        about_label.setFont(font)
        about_label.setAlignment(Qt.AlignCenter)  # Fixed NameError by importing Qt
        about_layout.addWidget(about_label)
        self.about_tab.setLayout(about_layout)

        # Set the layout for the main widget
        final_layout = QVBoxLayout()
        final_layout.addWidget(self.tabs)
        self.setLayout(final_layout)

    def get_rotors(self):
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

        rotor_order = [int(x) for x in self.order_input.text().split()]
        if len(set(rotor_order)) != len(rotor_order):
            QMessageBox.warning(self, "Input Error", "Rotor order must have unique values.")
            return []

        rotor_positions = [int(x) for x in self.position_input.text().split()]
        notch_positions = [int(x) for x in self.notch_input.text().split()]

        if len(rotor_order) != self.rotor_count_spinbox.value():
            QMessageBox.warning(self, "Input Error", f"You must select exactly {self.rotor_count_spinbox.value()} rotors.")
            return []

        if len(rotor_positions) != self.rotor_count_spinbox.value() or len(notch_positions) != self.rotor_count_spinbox.value():
            QMessageBox.warning(self, "Input Error", f"Positions and notches must match the number of rotors ({self.rotor_count_spinbox.value()}).")
            return []

        rotors = []
        for i in range(len(rotor_order)):
            rotor_number = str(rotor_order[i])
            if rotor_number in available_rotors:
                rotor = Rotor(available_rotors[rotor_number])
                rotor.set_position(rotor_positions[i])
                rotor.set_notch(notch_positions[i])
                rotors.append(rotor)
            else:
                QMessageBox.warning(self, "Input Error", f"Rotor {rotor_number} is not available.")
                return []

        return rotors

    def get_plugboard(self):
        plugboard_pairs = self.plugboard_input.text().upper()
        plugboard_dict = {}
        if plugboard_pairs:
            pairs = plugboard_pairs.split()
            for pair in pairs:
                if len(pair) == 2:
                    plugboard_dict[pair[0]] = pair[1]
                    plugboard_dict[pair[1]] = pair[0]
        return Plugboard(plugboard_dict)

    def encrypt_message(self):
        rotors = self.get_rotors()
        if not rotors:
            return
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = self.get_plugboard()
        enigma = EnigmaMachine(rotors, reflector, plugboard)
        message = self.message_input.toPlainText()
        encrypted_message = enigma.encrypt_decrypt(message)
        self.output_area.setText(f"Encrypted message: {encrypted_message}")

    def decrypt_message(self):
        rotors = self.get_rotors()
        if not rotors:
            return
        reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        plugboard = self.get_plugboard()
        enigma = EnigmaMachine(rotors, reflector, plugboard)
        message = self.message_input.toPlainText()
        decrypted_message = enigma.encrypt_decrypt(message)
        self.output_area.setText(f"Decrypted message: {decrypted_message}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EnigmaGUI()
    ex.show()
    sys.exit(app.exec_())
