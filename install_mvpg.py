import os
import sys
import shutil
import time
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import subprocess
import base64
from cryptography.fernet import Fernet

# Convert the custom key to a valid Fernet key using base64 encoding and padding
def get_encryption_key():
    custom_key = "&*28(2"
    # Pad the key to be at least 32 bytes long
    padded_key = custom_key.ljust(32, '0')
    # Encode and convert to base64
    return base64.urlsafe_b64encode(padded_key.encode()[:32])

ENCRYPTION_KEY = get_encryption_key()

def decrypt_file(encrypted_path, decrypted_path):
    try:
        f = Fernet(ENCRYPTION_KEY)
        with open(encrypted_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(decrypted_path, 'wb') as file:
            file.write(decrypted_data)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")
        return False

def check_mvpg_installed():
    home = str(Path.home())
    scripts_dir = os.path.join(home, 'AppData', 'Local', 'Programs', 'Python', 'Scripts')
    mvpg_path = os.path.join(scripts_dir, "mvpg.py")
    mvpg6_path = os.path.join(scripts_dir, "mvpg6.py")
    mvpg5_path = os.path.join(scripts_dir, "mvpg5.py")
    
    installed_versions = []
    if os.path.exists(mvpg_path):
        installed_versions.append("v7.3")
    if os.path.exists(mvpg6_path):
        installed_versions.append("v6.0")
    if os.path.exists(mvpg5_path):
        installed_versions.append("v5.0")
    
    return installed_versions

def uninstall_mvpg():
    try:
        home = str(Path.home())
        scripts_dir = os.path.join(home, 'AppData', 'Local', 'Programs', 'Python', 'Scripts')
        
        # Check if any version is installed
        installed_versions = check_mvpg_installed()
        if not installed_versions:
            messagebox.showinfo("Uninstall", "No MVPG versions are currently installed.")
            return
        
        # Create uninstall window
        uninstall_window = tk.Toplevel()
        uninstall_window.title("MVPG Uninstaller")
        uninstall_window.geometry("300x200")
        
        # Center the window
        window_width = 300
        window_height = 200
        screen_width = uninstall_window.winfo_screenwidth()
        screen_height = uninstall_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        uninstall_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        label = tk.Label(uninstall_window, text="Select version to uninstall:", font=("Arial", 12))
        label.pack(pady=20)
        
        def perform_uninstall(version):
            try:
                if version == "v7.3":
                    file_to_remove = "mvpg.py"
                    bat_to_remove = "mvpg.bat"
                elif version == "v6.0":
                    file_to_remove = "mvpg6.py"
                    bat_to_remove = "mvpg6.bat"
                else:  # v5.0
                    file_to_remove = "mvpg5.py"
                    bat_to_remove = "mvpg5.bat"
                
                # Remove files
                os.remove(os.path.join(scripts_dir, file_to_remove))
                os.remove(os.path.join(scripts_dir, bat_to_remove))
                
                messagebox.showinfo("Success", f"MVPG {version} has been uninstalled successfully!")
                uninstall_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error during uninstallation: {str(e)}")
        
        for version in installed_versions:
            btn = tk.Button(uninstall_window, 
                          text=f"Uninstall {version}", 
                          command=lambda v=version: perform_uninstall(v))
            btn.pack(pady=5)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error: {str(e)}")

def install_mvpg(version="v7.3"):
    # Check if already installed
    installed_versions = check_mvpg_installed()
    if version == "v7.3" and "v7.3" in installed_versions:
        messagebox.showinfo("Installation", "MVPG v7.3 is already installed!")
        return
    elif version == "v6.0" and "v6.0" in installed_versions:
        messagebox.showinfo("Installation", "MVPG v6.0 is already installed!")
        return
    elif version == "v5.0" and "v5.0" in installed_versions:
        messagebox.showinfo("Installation", "MVPG v5.0 is already installed!")
        return
    
    # Create the main window
    root = tk.Tk()
    root.title(f"MVPG {version} Installer")
    root.geometry("400x200")
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    # Create and pack widgets
    label = tk.Label(root, text=f"MVPG {version} Installation", font=("Arial", 14))
    label.pack(pady=20)
    
    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=20)
    
    status_label = tk.Label(root, text="Ready to install...")
    status_label.pack(pady=10)
    
    def perform_installation():
        try:
            # Get the Windows user's home directory
            home = str(Path.home())
            
            # Create Scripts directory if it doesn't exist
            scripts_dir = os.path.join(home, 'AppData', 'Local', 'Programs', 'Python', 'Scripts')
            os.makedirs(scripts_dir, exist_ok=True)
            
            # Update progress
            progress['value'] = 20
            status_label.config(text="Creating directories...")
            root.update()
            time.sleep(0.5)
            
            # Copy appropriate version file
            if version == "v7.3":
                source = "mvpg.py"
                destination = os.path.join(scripts_dir, "mvpg.py")
                bat_name = "mvpg.bat"
            elif version == "v6.0":
                source = "mvpg6.py"
                destination = os.path.join(scripts_dir, "mvpg6.py")
                bat_name = "mvpg6.bat"
            else:  # v5.0
                source = "mvpg5.py"
                destination = os.path.join(scripts_dir, "mvpg5.py")
                bat_name = "mvpg5.bat"
            
            shutil.copy2(source, destination)
            
            # Update progress
            progress['value'] = 50
            status_label.config(text="Copying files...")
            root.update()
            time.sleep(0.5)
            
            # Create batch file
            batch_path = os.path.join(scripts_dir, bat_name)
            with open(batch_path, 'w') as f:
                f.write('@echo off\n')
                f.write(f'python "{destination}" %*')
            
            # Update progress
            progress['value'] = 80
            status_label.config(text="Creating batch file...")
            root.update()
            time.sleep(0.5)
            
            # Add Scripts directory to PATH using PowerShell
            powershell_command = f'[Environment]::SetEnvironmentVariable("Path", $env:Path + ";{scripts_dir}", "User")'
            subprocess.run(["powershell", "-Command", powershell_command], capture_output=True)
            
            # Complete installation
            progress['value'] = 100
            status_label.config(text="Installation completed! Please restart your command prompt.")
            root.update()
            time.sleep(1)
            
            # Close the window after 3 seconds
            root.after(3000, root.destroy)
            
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
            root.update()
    
    # Create install button
    install_button = tk.Button(root, text="Install", command=perform_installation)
    install_button.pack(pady=10)
    
    root.mainloop()

def main():
    # Create main window
    root = tk.Tk()
    root.title("MVPG Installer")
    root.geometry("400x300")
    root.eval('tk::PlaceWindow . center')
    
    # Create and pack widgets
    label = tk.Label(root, text="MVPG Installer", font=("Arial", 16, "bold"))
    label.pack(pady=20)
    
    # Install latest version button
    install_latest_btn = tk.Button(root, 
                                 text="Install Latest (v7.3)", 
                                 command=lambda: install_mvpg("v7.3"))
    install_latest_btn.pack(pady=10)
    
    # Install v6.0 button
    install_v6_btn = tk.Button(root, 
                              text="Install v6.0", 
                              command=lambda: install_mvpg("v6.0"))
    install_v6_btn.pack(pady=10)
    
    # Install v5.0 button
    install_v5_btn = tk.Button(root, 
                              text="Install v5.0", 
                              command=lambda: install_mvpg("v5.0"))
    install_v5_btn.pack(pady=10)
    
    # Uninstall button
    uninstall_btn = tk.Button(root, 
                             text="Uninstall MVPG", 
                             command=uninstall_mvpg)
    uninstall_btn.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main() 