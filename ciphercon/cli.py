def main():
    import argparse
    from .core import encrypt, decrypt

    parser = argparse.ArgumentParser(prog="ciphercon")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("text")

    args = parser.parse_args()

    if args.mode == "encrypt":
        print(encrypt(args.text))
    else:
        print(decrypt(args.text))