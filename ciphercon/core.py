import base64
import os
import json
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# =========================
# Config path
# =========================
config_path = Path.home() / ".ciphercon"
config_path.mkdir(exist_ok=True)


# =========================
# Key derivation (for passwords)
# =========================
def _derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return kdf.derive(password)


# =========================
# Setup RSA keys
# =========================
def setup():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    (config_path / "private_key.pem").write_bytes(private_pem)

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    (config_path / "public_key.pem").write_bytes(public_pem)


# =========================
# RSA
# =========================
def __asymmetric_encrypt(plaintext: bytes, publicKey: bytes) -> bytes:
    public_key = serialization.load_pem_public_key(publicKey)

    ciphertext = public_key.encrypt( # pyright: ignore[reportAttributeAccessIssue]
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return base64.b64encode(ciphertext)


def __asymmetric_decrypt(ciphertext: bytes, privateKey: bytes) -> bytes:
    private_key = serialization.load_pem_private_key(
        privateKey,
        password=None,
    )

    return private_key.decrypt( # pyright: ignore[reportAttributeAccessIssue]
        base64.b64decode(ciphertext),
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


# =========================
# AES-GCM (safe)
# =========================
def aes_encrypt(plaintext: bytes, key: bytes | None) -> bytes:
    if not key:
        return plaintext

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return base64.b64encode(nonce + ciphertext)


def aes_decrypt(ciphertext: bytes, key: bytes | None) -> bytes:
    if not key:
        return ciphertext

    data = base64.b64decode(ciphertext)
    nonce = data[:12]
    ct = data[12:]

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ct, None)


# =========================
# Connection class
# =========================
class Connection:
    def __init__(self, name: str, password: str | None = None) -> None:
        self.name = name
        self.password = password
        self.symmetricKey: bytes | None = None

    def encrypt(self, plaintext: bytes) -> bytes:
        if not self.symmetricKey:
            raise ValueError("No symmetric key loaded")
        return aes_encrypt(plaintext, self.symmetricKey)

    def decrypt(self, ciphertext: bytes) -> bytes:
        if not self.symmetricKey:
            raise ValueError("No symmetric key loaded")
        return aes_decrypt(ciphertext, self.symmetricKey)

    def _register(self, symmetricKey: bytes):
        self.symmetricKey = symmetricKey

        data = {"key": base64.b64encode(symmetricKey).decode()}

        if self.password:
            salt = os.urandom(16)
            key = _derive_key(self.password.encode(), salt)

            encrypted = aes_encrypt(json.dumps(data).encode(), key)

            payload = {
                "salt": base64.b64encode(salt).decode(),
                "data": encrypted.decode(),
            }

            (config_path / f"{self.name}.enc").write_text(json.dumps(payload))
        else:
            (config_path / f"{self.name}.json").write_text(json.dumps(data))

    def _load_key(self):
        if self.password:
            path = config_path / f"{self.name}.enc"
            if not path.exists():
                raise FileNotFoundError("Encrypted key not found")

            payload = json.loads(path.read_text())

            salt = base64.b64decode(payload["salt"])
            key = _derive_key(self.password.encode(), salt)

            decrypted = aes_decrypt(payload["data"].encode(), key)
            data = json.loads(decrypted)

            self.symmetricKey = base64.b64decode(data["key"])

        else:
            path = config_path / f"{self.name}.json"
            if not path.exists():
                raise FileNotFoundError("Key not found")

            data = json.loads(path.read_text())
            self.symmetricKey = base64.b64decode(data["key"])


# =========================
# Connection API
# =========================
def create_connection(name: str, othersPublicKey: bytes, password=None):
    symmetricKey = os.urandom(32)

    encryptedSymmetricKey = __asymmetric_encrypt(
        symmetricKey, othersPublicKey
    )

    conn = Connection(name, password)
    conn._register(symmetricKey)

    return conn, encryptedSymmetricKey


def finish_connection(name, encryptedSymmetricKey, password=None):
    private_key_pem = (config_path / "private_key.pem").read_bytes()

    symmetricKey = __asymmetric_decrypt(
        encryptedSymmetricKey, private_key_pem
    )

    conn = Connection(name, password)
    conn._register(symmetricKey)

    return conn


def get_connection(name, password=None):
    conn = Connection(name, password)
    conn._load_key()
    return conn


# =========================
# Key access
# =========================
def get_public_key() -> bytes:
    return (config_path / "public_key.pem").read_bytes()


def _get_private_key() -> bytes:
    return (config_path / "private_key.pem").read_bytes()


# =========================
# CLI helpers (testing only)
# =========================
def encrypt(plaintext: bytes) -> bytes:
    key = b"0123456789abcdef0123456789abcdef"  # exactly 32 bytes  # OK for testing
    return aes_encrypt(plaintext, key)


def decrypt(ciphertext: bytes) -> bytes:
    key = b"0123456789abcdef0123456789abcdef"  # exactly 32 bytes  # OK for testing
    return aes_decrypt(ciphertext, key)