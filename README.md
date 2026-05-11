# Ciphercon v1.2.1

Secure peer-to-peer encryption library using **AES-256-GCM** (symmetric) and **RSA-2048** (asymmetric) encryption.
## Creators

[![Static Badge](https://img.shields.io/badge/noone--075-556B2F)](https://github.com/noone-075)

With help from:

[![Static Badge](https://img.shields.io/badge/sovietdevelopment-FF3322)](https://github.com/sovietdevelopment)

## Features

- ***AES-256-GCM***: Authenticated symmetric encryption for fast, secure messaging
- ***RSA-2048 with OAEP***: Asymmetric encryption for secure key exchange
- ***PBKDF2-HMAC-SHA256***: Password-based key derivation for encrypted storage
- ***Persistent connections***: Store encrypted symmetric keys locally
- ***CLI & API***: Use as a library or command-line tool
- ***GUI***: Use the library as a every day tool with a pre-made gui
- ***Type hints***: Full type annotations for better IDE support

## Installation

if we set up the pip thing
```bash
pip install ciphercon
```
or download the lastest .whl in the [releases](https://github.com/noone-075/ciphercon/releases) then install the package
```bash
pip install ciphercon-<version>-py3-none-any.whl
```

## Quick Start

### Setup (Generate RSA Keys)

```python
from ciphercon import setup, get_public_key

# Generate RSA-2048 key pair
setup()

# Get your public key to share
public_key = get_public_key()
print(public_key.decode())
```

### Create a Connection (Sender)

```python
from ciphercon import create_connection

# Create connection with recipient's public key
conn, encrypted_key = create_connection(
    name="alice",
    othersPublicKey=alice_public_key_bytes,
    password="optional_password"
)

# Send the encrypted_key to Alice
print(encrypted_key.decode())
```

### Finish Connection (Recipient)

```python
from ciphercon import finish_connection

# Receive the encrypted symmetric key from sender
conn = finish_connection(
    name="bob",
    encryptedSymmetricKey=encrypted_key_from_bob,
    password="optional_password"
)
```

### Encrypt & Decrypt

```python
# Encrypt a message
encrypted = conn.encrypt(b"Hello, Alice!")

# Decrypt a message
decrypted = conn.decrypt(encrypted)
print(decrypted.decode())  # "Hello, Alice!"
```

### Load Existing Connection

```python
from ciphercon import get_connection

conn = get_connection(name="alice", password="optional_password")
encrypted = conn.encrypt(b"Message")
```

## CLI Usage

### Generate RSA keys
```bash
ciphercon setup
```

### Get the RSA public key
```bash
ciphercon key
```

### Create a new connection
```bash
ciphercon create alice
```

### Finish a connection
```bash
ciphercon finish alice
```

### Connect and communicate
```bash
ciphercon connect alice
> encrypt hello world
> decrypt <encrypted_text>
```

### GUI Usage
After installing the package, launch the graphical tool with:
```bash
ciphercon-gui
```

If you build a Windows executable, point it at `ciphercon/gui.py` or the `ciphercon-gui` entry point.

## API Reference

### Functions

- `setup()` - Generate RSA-2048 key pair
- `get_public_key() -> bytes` - Get your public key
- `create_connection(name, othersPublicKey, password=None) -> (Connection, bytes)` - Create peer connection
- `finish_connection(name, encryptedSymmetricKey, password=None) -> Connection` - Accept peer connection
- `get_connection(name, password=None) -> Connection` - Load saved connection

### Connection Class

```python
class Connection:
    def encrypt(self, plaintext: bytes) -> bytes
    def decrypt(self, ciphertext: bytes) -> bytes
```

## Security Notes

- **RSA-2048**: Used only for initial key exchange, not for message encryption
- **AES-256-GCM**: Provides authenticated encryption with 256-bit keys
- **Nonce/IV**: Random 12-byte nonce generated per message
- **Key Storage**: Symmetric keys stored encrypted with PBKDF2 if password provided
- **No Perfect Forward Secrecy**: Compromised symmetric key reveals all messages

## File Structure

Keys are stored in `~/.ciphercon/`:
- `private_key.pem` - Your private RSA key
- `public_key.pem` - Your public RSA key
- `{name}.json` - Unencrypted symmetric key
- `{name}.enc` - Password-encrypted symmetric key

## Requirements

- Python 3.12+
- cryptography >= 41.0.0

## License

MIT License - See LICENSE file
