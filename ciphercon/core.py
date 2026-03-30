from pathlib import Path

config_path = Path.home() / ".ciphercon"


def setup():
    # creating a private + public key pair
    pass


def __asymmetric_encrypt(plaintext: str, publicKey: str) -> str:
    # encrypt the plaintext with the public key and return the ciphertext
    return "asymmetric_ciphertext"


def __asymmetric_decrypt(ciphertext: str, privateKey: str) -> str:
    # decrypt the ciphertext with the private key and return the plaintext
    return "asymmetric_plaintext"


def __encrypt(plaintext: str, key: str | None) -> str:
    # encrypt the plaintext with the key and return the ciphertext
    return "ciphertext"


def __decrypt(ciphertext: str, key: str | None) -> str:
    # decrypt the ciphertext with the key and return the plaintext
    return "plaintext"


class Connection:
    def __init__(self, name, password=None) -> None:
        self.name = name
        self.password = password

    def encrypt(self, plaintext: str) -> str:
        # encrypt the plaintext with the symmetric key and return the ciphertext
        return __encrypt(plaintext, self.symmetricKey)

    def decrypt(self, ciphertext: str) -> str:
        # decrypt the ciphertext with the symmetric key and return the plaintext
        return __decrypt(ciphertext, self.symmetricKey)

    def __register(self, symmetricKey):
        # register the connection in storage
        self.symmetricKey = symmetricKey
        cryptedKey = __encrypt("KEY:" + symmetricKey, self.password)
        (config_path / self.name).write_text(cryptedKey)

    def __load_key(self):
        # load the symmetric key from storage
        cryptedKey = (config_path / self.name).read_text()
        rawKey = __decrypt(cryptedKey, self.password)
        if not rawKey.startswith("KEY:"):
            raise ValueError("Invalid key format / Wrong password")
        self.symmetricKey = rawKey[4:]  # Remove "KEY:" prefix


def create_connection(name, othersPublicKey, password=None) -> tuple[Connection, str]:
    # create a random symmetric key and encrypt it with the other person's public key
    symmetricKey = "symmetric_key"
    encryptedSymmetricKey = __asymmetric_encrypt(symmetricKey, othersPublicKey)
    connection = Connection(name, password)
    connection.__register(symmetricKey)
    return connection, encryptedSymmetricKey


def finish_connection(name, encryptedSymmetricKey, password=None) -> Connection:
    # decrypt the symmetric key with our private key and store it for later use
    symmetricKey = __asymmetric_decrypt(encryptedSymmetricKey, __get_private_key())
    connection = Connection(name, password)
    connection.__register(symmetricKey)
    return connection


def get_connection(name, password=None) -> Connection:
    connection = Connection(name, password)
    connection.__load_key()
    return connection


def get_public_key() -> str:
    # give our public key to the other person
    return "public_key"


def __get_private_key() -> str:
    # get our private key to decrypt the symmetric key sent by the other person
    return "private_key"
