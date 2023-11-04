import os
from colorama import Fore 
import sqlite3
import bcrypt
from cryptography.fernet import Fernet

# Specify that the files are in the 'cred' folder
cred_folder = 'cred'
key_file = os.path.join(cred_folder, 'encryption.key')

print(f"""
      
███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗                   ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗     ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗ 
██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║                   ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗
███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║         █████╗    ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝
╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║         ╚════╝    ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗
███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗              ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝    ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝              ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
        made by https://github.com/Rud3p 
      """)

if os.path.exists(key_file):
    with open(key_file, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)

f = Fernet(key)

db_file = os.path.join(cred_folder, 'passwords.db')
conn = sqlite3.connect(db_file)
c = conn.cursor()

try:
    c.execute("""CREATE TABLE users  
              (id INTEGER PRIMARY KEY,  
               username TEXT, 
               password TEXT)""")
except sqlite3.OperationalError:
    pass

try:
    c.execute("""CREATE TABLE passwords  
              (id INTEGER PRIMARY KEY,
               website TEXT,
               username TEXT,  
               email TEXT,
               password BLOB)""")
except sqlite3.OperationalError:
    pass

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users VALUES (NULL, ?, ?)", (username, hashed_password))
    conn.commit()

def verify_password(username, password):
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = c.fetchone()
    if stored_password is not None:
        return bcrypt.checkpw(password.encode('utf-8'), stored_password[0]) 
    return False

def add_password(website, username, email, password):
    encrypted_password = f.encrypt(password.encode())
    c.execute("INSERT INTO passwords VALUES (NULL, ?, ?, ?, ?)", 
            (website, username, email, encrypted_password))
    conn.commit()

def view_passwords():
    c.execute('SELECT * FROM passwords')
    rows = c.fetchall()

    print("{:<20} {:<20} {:<20} {:<30}".format('Website', 'Username', 'Email', 'Password'))
    print("{:<20} {:<20} {:<20} {:<30}".format('-'*20, '-'*20, '-'*20, '-'*30))

    for row in rows:
        password = f.decrypt(row[4]).decode()
        print("{:<20} {:<20} {:<20} {:<30}".format(row[1], row[2], row[3], password))

while True:
    print("1. Register")
    print("2. Login")
    choice = input("> ")

    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        register_user(username, password)

    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")

        if verify_password(username, password):
            print("\nLogged In")

            while True:
                print("1. Add Password")
                print("2. View Passwords")
                print("3. Logout")
                choice = input("> ")

                if choice == "1":
                    add_password(input("Website: "), input("Username: "), input("Email: "), input("Password: "))
                elif choice == "2":
                    view_passwords()
                elif choice == "3":
                    print("\nLogged Out")
                    break
        else:
            print("\nInvalid Credentials")
