# Enigma

A C++ implementation of a simplified Enigma M3 machine.

## Requirements

- A C++17-compatible compiler
- CMake 3.10 or newer

## Build

```sh
mkdir build
cd build
cmake ..
cmake --build .
```

## Usage

Run the executable from the build directory:

```sh
./enigma
```

Enter text when prompted. The same settings and key can be used to encrypt and decrypt text.

## Project Structure

- `src/` — C++ source files
- `include/` — header files
- `tests/` — unit tests, if included

## License

See the repository for license information.

## Notes

- This implementation is a simplified version of the historical Enigma machine and may not include all features of the original device.
- The encryption is symmetric; the same key and settings must be used for both encryption and decryption.
- Ensure that the input text only contains characters supported by the machine's configuration.
- The machine does not handle spaces, punctuation, or special characters outside its defined alphabet.

## Enigma Machine Configuration

- Five rotors, three of which are used at a time
- A reflector
- A plugboard for additional encryption

