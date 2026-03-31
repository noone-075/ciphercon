"""Ciphercon: Simple cipher tool with AES and RSA encryption.

This module provides symmetric (AES-256-GCM) and asymmetric (RSA-2048) encryption.

Basic usage:
    from ciphercon import setup, create_connection, finish_connection, get_connection
    
    # Generate RSA key pair
    setup()
    
    # Create connection with other person
    conn, encrypted_key = create_connection("alice", alice_public_key)
    
    # On the other side, finish the connection
    conn = finish_connection("bob", encrypted_key, password="secret")
    
    # Encrypt and decrypt messages
    encrypted = conn.encrypt(b"Hello World")
    plaintext = conn.decrypt(encrypted)
"""

from .core import (
    Connection,
    create_connection,
    finish_connection,
    get_connection,
    get_public_key,
    setup,
    # encrypt,
    # decrypt,
)

__all__ = [
    "Connection",
    "create_connection",
    "finish_connection",
    "get_connection",
    "get_public_key",
    "setup",
    # "encrypt",
    # "decrypt",
]
__version__ = "0.1.0"