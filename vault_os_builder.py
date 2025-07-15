# vault_os_builder.py
# Full stack: Includes branding, bootable USB image simulation, and visual splash screen

import os
import shutil
import qrcode

VAULT_DIR = "vault_os_build"
ISO_NAME = "vault_os_custom.iso"

# Step 1: Prepare directories
def prepare_workspace():
    print("[+] Setting up build workspace...")
    os.makedirs(VAULT_DIR, exist_ok=True)
    os.makedirs(os.path.join(VAULT_DIR, "iso_root"), exist_ok=True)
    os.makedirs(os.path.join(VAULT_DIR, "custom_files"), exist_ok=True)
    os.makedirs(os.path.join(VAULT_DIR, "branding"), exist_ok=True)

# Step 2: Simulate download of base ISO
def simulate_download_base_iso():
    print("[+] Simulating base ISO download...")
    iso_path = os.path.join(VAULT_DIR, "base.iso")
    with open(iso_path, "w") as f:
        f.write("Simulated Debian ISO content.")
    print(f"[+] Simulated base ISO created: {iso_path}")

# Step 3: Add QR encryption tool
def generate_qr_tool():
    print("[+] Generating QR encryption tool script...")
    tool_code = '''
import qrcode

def generate_qr():
    text = input("Enter secure message: ")
    img = qrcode.make(text)
    img.save("secure_message.png")
    print("QR code saved as secure_message.png")

if __name__ == '__main__':
    generate_qr()
'''
    tool_path = os.path.join(VAULT_DIR, "custom_files", "qr_tool.py")
    with open(tool_path, "w") as f:
        f.write(tool_code)

# Step 4: Add encrypted file vault tool
def generate_encryption_tool():
    print("[+] Generating file encryption/decryption tool...")
    tool_code = '''
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import os

def get_key(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def encrypt(filename, password):
    key = get_key(password)
    chunk_size = 64 * 1024
    output_file = filename + ".enc"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(output_file, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                outfile.write(encryptor.encrypt(chunk))
    print(f"Encrypted file saved as: {output_file}")

def decrypt(filename, password):
    key = get_key(password)
    chunk_size = 64 * 1024
    output_file = filename.replace(".enc", ".dec")

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(output_file, 'wb') as outfile:
            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)
    print(f"Decrypted file saved as: {output_file}")

if __name__ == '__main__':
    mode = input("Encrypt or Decrypt (e/d)? ")
    fname = input("File path: ")
    pw = input("Password: ")
    if mode.lower() == 'e':
        encrypt(fname, pw)
    else:
        decrypt(fname, pw)
'''
    tool_path = os.path.join(VAULT_DIR, "custom_files", "vault_encryptor.py")
    with open(tool_path, "w") as f:
        f.write(tool_code)

# Step 5: Add offline help guide
def generate_help_docs():
    print("[+] Writing offline help documentation...")
    doc_text = '''
Vault OS - Offline Survival Docs

1. QR Tool:
    - Run qr_tool.py to generate secure QR messages.

2. File Encryption:
    - Use vault_encryptor.py to encrypt/decrypt local files.

3. Boot:
    - Insert USB. Reboot machine. Boot from USB.

4. Important:
    - NEVER connect Vault OS to any network.
    - Store your credentials physically, not digitally.
    - Do not modify system files outside of /vault.
'''
    with open(os.path.join(VAULT_DIR, "custom_files", "README_HELP.txt"), "w") as f:
        f.write(doc_text)

# Step 6: Add launcher script
def generate_launcher():
    print("[+] Creating launcher script...")
    launcher_code = '''
#!/bin/bash
clear
echo "========================="
echo "   VAULT OS LAUNCHER   "
echo "========================="
echo "1. Run QR Tool"
echo "2. Run Encryptor"
echo "Enter option: "
read opt
if [ "$opt" == "1" ]; then
    python3 qr_tool.py
elif [ "$opt" == "2" ]; then
    python3 vault_encryptor.py
else
    echo "Invalid option."
fi
'''
    with open(os.path.join(VAULT_DIR, "custom_files", "launcher.sh"), "w") as f:
        f.write(launcher_code)

# Step 7: Generate branding splash screen
def generate_branding():
    print("[+] Creating branding splash file...")
    splash = os.path.join(VAULT_DIR, "branding", "VAULT_OS_SPLASH.txt")
    with open(splash, "w") as f:
        f.write("""
 __     ______  _    _   ____   _____ _____ \
 \ \   / / __ \| |  | | |  _ \ |_   _| ____|
  \ \ / / |  | | |  | | | |_) | | | |  _|  
   \ V /| |__| | |__| | |  __/  | | | |___ 
    \_/  \____/ \____/  |_|     |_| |_____|

      AIR-GAPPED SECURITY SUITE v1.0
""")

# Step 8: Copy files to ISO root
def add_custom_tools():
    print("[+] Adding tools and docs to ISO root...")
    tools_src = os.path.join(VAULT_DIR, "custom_files")
    tools_dst = os.path.join(VAULT_DIR, "iso_root", "vault")
    os.makedirs(tools_dst, exist_ok=True)
    for file_name in os.listdir(tools_src):
        shutil.copy(os.path.join(tools_src, file_name), tools_dst)
    splash_src = os.path.join(VAULT_DIR, "branding", "VAULT_OS_SPLASH.txt")
    shutil.copy(splash_src, os.path.join(VAULT_DIR, "iso_root", "vault"))

# Step 9: Simulate ISO creation
def simulate_build_iso():
    print("[+] Simulating ISO build process...")
    output_path = os.path.join(VAULT_DIR, ISO_NAME)
    with open(output_path, "w") as f:
        f.write("This is a placeholder for the actual ISO image.")
    print(f"[+] Vault OS ISO placeholder created at: {output_path}")

# Main execution
if __name__ == "__main__":
    prepare_workspace()
    simulate_download_base_iso()
    generate_qr_tool()
    generate_encryption_tool()
    generate_help_docs()
    generate_launcher()
    generate_branding()
    add_custom_tools()
    simulate_build_iso()
