"""
This python module provides prototype functions for encrypting and decrypting files using the AES encryption
algorithm in Cipher Feedback (CFB) mode. The encryption key is derived from a user-provided password using the
PBKDF2 key derivation function.

Usage:
    To encrypt and decrypt a file, run the script with the following command:
    $ python3 encrypt_decrypt.py <input_file> <password>

    The encrypted file will be saved as '<input_file>.enc', and the decrypted file will be saved as
    '<input_file>_decrypted.txt'.

Requirements:
    - Python 3
    - requirements.txt
"""

import os
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode, urlsafe_b64decode


def generate_key(password, salt=None):
    """
        Generates a cryptographic key using PBKDF2 key derivation function.
        Parameters:
            password (str): The password from which to derive the key.
            salt (bytes, optional): A random salt used in the key derivation process. If not provided, a random salt is generated.
        Returns:
            Tuple[bytes, bytes]: A tuple containing the derived key and the salt used in the process.
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key, salt


def encrypt_file(input_file, output_file, password):
    """
       Encrypts a file using AES encryption algorithm in CFB mode.
       Parameters:
           input_file (str): The path to the input file to be encrypted.
           output_file (str): The path to save the encrypted output file.
           password (str): The password used for key derivation.

    """
    try:
        key, salt = generate_key(password)
        iv = os.urandom(16)

        with open(input_file, 'rb') as f:
            plaintext = f.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        with open(output_file, 'wb') as f:
            f.write(salt + iv + ciphertext)

        print(f"File '{input_file}' encrypted and saved as '{output_file}'")
    except Exception as e:
        print(f"Error encrypting file: {e}")


def decrypt_file(input_file, output_file, password):
    """
        Decrypt an encrypted file using AES encryption algorithm in CFB mode.
        Parameters:
            input_file (str): The path to the encrypted input file.
            output_file (str): The path to save the decrypted output file.
            password (str): The password used for key derivation.
    """
    try:
        with open(input_file, 'rb') as f:
            data = f.read()

        salt = data[:16]
        iv = data[16:32]
        ciphertext = data[32:]

        key, _ = generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        with open(output_file, 'wb') as f:
            f.write(plaintext)

        print(f"File '{input_file}' decrypted and saved as '{output_file}'")
    except Exception as e:
        print(f"Error decrypting file: {e}")


# Example of usage in main
if __name__ == "__main__":
    try:
        if len(sys.argv) != 3:
            print("Usage: python encrypt_decrypt.py <input_file> <password>")
            sys.exit(1)

        input_file = os.path.abspath(sys.argv[1])
        password = sys.argv[2]

        encrypted_file = f'{input_file}.enc'
        decrypted_file = f'{input_file}_decrypted.txt'

        # Encrypt the file
        encrypt_file(input_file, encrypted_file, password)

        # Decrypt the file
        decrypt_file(encrypted_file, decrypted_file, password)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")