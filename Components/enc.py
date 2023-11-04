import os
from colorama import Fore
import base64
from cryptography.fernet import Fernet
from Crypto.Cipher import Blowfish

print(f"""
      
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗                   ████████╗███████╗██╗  ██╗████████╗    ███████╗███╗   ██╗ ██████╗    ██╗██████╗ ███████╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ ██████╗ 
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║                   ╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝    ██╔════╝████╗  ██║██╔════╝   ██╔╝██╔══██╗██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║         █████╗       ██║   █████╗   ╚███╔╝    ██║       █████╗  ██╔██╗ ██║██║       ██╔╝ ██║  ██║█████╗  ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║██████╔╝
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║         ╚════╝       ██║   ██╔══╝   ██╔██╗    ██║       ██╔══╝  ██║╚██╗██║██║      ██╔╝  ██║  ██║██╔══╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║██╔══██╗
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗                 ██║   ███████╗██╔╝ ██╗   ██║       ███████╗██║ ╚████║╚██████╗██╔╝   ██████╔╝███████╗╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝██║  ██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝                 ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝       ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝    ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═╝
        made by https://github.com/Rud3p                                                                                                                                                                                                                                

            """)

def aes_encrypt(key, text):
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return encrypted_text

def aes_decrypt(key, text):
    fernet = Fernet(key)
    decrypted_text = fernet.decrypt(text)
    return decrypted_text.decode()

def blowfish_encrypt(key, text):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    while len(text) % 8 != 0:
        text += b' ' 
    encrypted_text = cipher.encrypt(text)
    return encrypted_text

def blowfish_decrypt(key, text):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    decrypted_text = cipher.decrypt(text)
    return decrypted_text.rstrip(b' ')  

def base64_encode(text):
    return base64.b64encode(text)

def base64_decode(text):
    return base64.b64decode(text)

# Option 1: Encrypt a message
def encrypt_message():
    message = input("Enter the message to encrypt: ")

    # Step 1: AES Encryption
    aes_key = Fernet.generate_key()
    aes_encrypted = aes_encrypt(aes_key, message)

    # Step 2: Blowfish Encryption
    blowfish_key = os.urandom(8)  # 8-byte Blowfish key
    blowfish_encrypted = blowfish_encrypt(blowfish_key, aes_encrypted)

    # Step 3: Base64 Encoding
    final_encrypted = base64_encode(blowfish_key + blowfish_encrypted)

    print(f"Encrypted message: {final_encrypted.decode()}")
    print(f"AES Key: {aes_key.decode()}")
    print(f"Blowfish Key: {base64.b64encode(blowfish_key).decode()}")

# Option 2: Decrypt a message
def decrypt_message():
    encrypted_message = input("Enter the encrypted message: ")
    aes_key = input("Enter the AES key: ").encode()
    blowfish_key_base64 = input("Enter the Blowfish key (in base64): ")
    blowfish_key = base64.b64decode(blowfish_key_base64)

    # Step 3: Base64 Decoding
    data = base64_decode(encrypted_message)

    # Step 2: Blowfish Decryption
    blowfish_decrypted = blowfish_decrypt(blowfish_key, data[8:])

    # Step 1: AES Decryption
    decrypted_message = aes_decrypt(aes_key, blowfish_decrypted)

    print(f"Decrypted message: {decrypted_message}")

while True:
    print("Options:")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    choice = input("Enter your choice: ")

    if choice == "1":
        encrypt_message()
    elif choice == "2":
        decrypt_message()
    else:
        print("Invalid choice. Please select a valid option.")
