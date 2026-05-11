"""Ciphercon: Simple cipher tool with AES and RSA encryption.

This module provides symmetric (AES-256-GCM) and asymmetric (RSA-2048) encryption.

Basic usage:
    from ciphercon import setup, create_connection, finish_connection, get_connection, connection_list
    
    # Generate RSA key pair
    setup()
    
    # Create connection with other person
    conn, encrypted_key = create_connection("alice", alice_public_key)
    
    # On the other side, finish the connection
    conn = finish_connection("bob", encrypted_key, password="secret")

    # after setting up the connection, you can use it to encrypt and decrypt messages
    active_connections = connection_list()  # List all active connections

    conn = get_connection("bob", password="secret")
    
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
    connection_list
)

__all__ = [
    "Connection",
    "create_connection",
    "finish_connection",
    "get_connection",
    "get_public_key",
    "setup",
    "connection_list"
]
__version__ = "1.2.2"
