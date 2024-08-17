# Enigma Machine

## About

This project is a Python-based graphical simulation of the Enigma Machine, a cipher device famously used by the Germans during World War II. The Enigma Machine was a significant piece of cryptographic equipment that encrypted and decrypted secret messages. This simulator allows users to understand and explore the mechanics behind this historical machine through a user-friendly graphical interface.

## Features

- **Rotors Configuration**: Users can select between 1 to 100 rotors, each with customizable wiring, positions, and notches. The rotor order, initial positions, and notch positions are fully configurable.
  
- **Custom Reflector**: The simulator provides an option to use a custom reflector. Users can enable this feature and input their custom wiring for the reflector, or opt for the default reflector.

- **Plugboard Setup**: The simulator includes a plugboard configuration, where users can define multiple letter pairs for swapping, simulating the real-world plugboard functionality.

- **Message Encryption/Decryption**: The core functionality of the Enigma Machine is maintained. Users can encrypt and decrypt messages by configuring the rotors, reflector, and plugboard settings.

- **Interactive GUI**: The program features a PyQt5-based graphical user interface, making it easy to interact with the different components of the Enigma Machine. The GUI includes a main tab for operations and an "About" tab for information about the program.

## Capabilities

- **Simulation Accuracy**: The simulator closely mimics the behavior of the original Enigma Machine, allowing users to explore how different configurations impact the encryption and decryption of messages.

- **Flexible Configuration**: The program is highly configurable, giving users control over the rotors, reflector, and plugboard, allowing them to experiment with various encryption schemes.

- **Educational Tool**: This simulator serves as an educational tool for anyone interested in cryptography and the history of the Enigma Machine. It provides hands-on experience with one of the most famous cryptographic devices in history.

## How to Use

1. **Rotors Selection**: Choose the number of rotors you want to use (1-100) and configure their order, initial positions, and notch positions.

2. **Custom Reflector**: Decide whether to use a custom reflector. If "Yes" is selected, input the custom wiring for the reflector (26 unique uppercase letters).

3. **Plugboard Configuration**: Enter the plugboard settings by defining letter pairs (e.g., `AB CD EF`).

4. **Encrypt/Decrypt**: Input the message you wish to encrypt or decrypt, and click the respective button to see the result.
