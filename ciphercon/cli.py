# hi noone, if I forgot to add colors to any messages, just tell me 

# =========================
# COLOR CONVENTIONS
# =========================

# RED: ERROR MSG
# GREEN: SUCCESSFUL ACTIONS
# MAGENTA: DISCONNECT
# CYAN: FILE OPERATIONS
# YELLOW: HELP

# =========================
# IMPORTS
# =========================

import sys
import tempfile
from pathlib import Path

from colorama import (
Fore,
Back,
Style
)

from .core import (
    create_connection,
    finish_connection,
    get_connection,
    get_public_key,
    setup
)

init(autoreset=True)

# =========================
# Helpers
# =========================
def ask(prompt: str) -> str:
    return input(prompt).strip()


def read_multiline(prompt: str) -> bytes:
    print(prompt + " (Ctrl+Z to finish):")
    return sys.stdin.read().encode()


def is_file_path(text: str) -> Path | None:
    p = Path(text)
    return p if p.exists() and p.is_file() else None

# =========================
# Commands
# =========================
def cmd_create(name: str):
    pubkey = read_multiline("Paste OTHER person's public key")
    password = ask(Style.BRIGHT + Fore. + "Password (optional): ") or None

    conn, encrypted_key = create_connection(name, pubkey, password)

    print(Style.BRIGHT + Fore.GREEN + "\nConnection created.")
    print(Style.BRIGHT + Fore.YELLOW + "\nSend this encrypted symmetric key to the other person:\n")
    print(encrypted_key.decode())


def cmd_finish(name: str):
    encrypted_key = read_multiline("Paste encrypted symmetric key")
    password = ask("(Optional) password: ") or None

    finish_connection(name, encrypted_key, password)

    print(Style.BRIGHT + Fore.GREEN + "Connection finished.")


def cmd_key():
    print(get_public_key().decode())


def cmd_connect(name: str):
    password = ask("Password (optional): ") or None

    conn = get_connection(name, password)

    print(Style.BRIGHT + Fore.GREEN + f"Connected to '{name}'")
    print(Style.BRIGHT + Fore.YELLOW + "Type messages. Ctrl+D to exit.\n")

    try:
        while True:
            text = input("CIPHERCON-> ")

            if text.startswith("encrypt "):
                data = text[len("encrypt ") :]

                file_path = is_file_path(data)
                if file_path:
                    content = file_path.read_bytes()
                    encrypted = conn.encrypt(content)

                    tmp = tempfile.NamedTemporaryFile(delete=False)
                    tmp.write(encrypted)
                    tmp.close()

                    print(Style.BRIGHT + Fore.CYAN + f"Encrypted file → {tmp.name}")
                else:
                    encrypted = conn.encrypt(data.encode())
                    print(encrypted.decode())

            elif text.startswith("decrypt "):
                data = text[len("decrypt ") :]

                file_path = is_file_path(data)
                if file_path:
                    content = file_path.read_bytes()
                    decrypted = conn.decrypt(content)

                    tmp = tempfile.NamedTemporaryFile(delete=False)
                    tmp.write(decrypted)
                    tmp.close()

                    print(Style.BRIGHT + Fore.CYAN + f" Decrypted file → {tmp.name}")
                else:
                    decrypted = conn.decrypt(data.encode())
                    print(decrypted.decode(errors="ignore"))

            else:
                print(Style.BRIGHT + Fore.CYAN + "Commands: encrypt <text|file>, decrypt <text|file>")

    except EOFError:
        print(Style.BRIGHT + Fore.MAGENTA +  + "\nDisconnected.")


# =========================
# Entry point
# =========================
def main():
    if len(sys.argv) < 2:
        print(Style.BRIGHT + Fore.RED + "Usage: ciphercon <command> [args]")
        return

    cmd = sys.argv[1]

    if cmd == "setup":
        setup()

    elif cmd == "create" and len(sys.argv) >= 3:
        cmd_create(sys.argv[2])

    elif cmd == "finish" and len(sys.argv) >= 3:
        cmd_finish(sys.argv[2])

    elif cmd == "key":
        cmd_key()

    elif cmd == "connect" and len(sys.argv) >= 3:
        cmd_connect(sys.argv[2])

    else:
        print("Commands:")
        print(Fore.BLUE + " - ciphercon create <name>")
        print(Fore.BLUE + " - ciphercon finish <name>")
        print(Fore.BLUE + " - ciphercon key")
        print(Fore.BLUE + " - ciphercon connect <name>")


if __name__ == "__main__":
    main()
