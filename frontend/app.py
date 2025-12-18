import customtkinter as ctk
from tkinter import filedialog
import subprocess
import os
import threading
import time
import sys
from PIL import Image  # Image handle karne ke liye

# --- Setup ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("600x500")
        self.title("Shield Pro")
        self.resizable(True, True)

        try:
            # Icon ka path nikalo
            icon_path = resource_path(os.path.join("assets", "icon.ico"))
            
            # Window par icon set karo
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon error: {e}")

        # Start with Splash Screen
        self.show_splash_screen()

    def show_splash_screen(self):
        self.splash_frame = ctk.CTkFrame(self, width=600, height=500, fg_color="#1a1a1a")
        self.splash_frame.pack(fill="both", expand=True)

        # --- IMAGE LOGIC (Updated) ---
        try:
            # Image load karne ka path (Assets folder se)
            img_path = resource_path(os.path.join("assets", "logo.png"))
            
            # Image ko load karo aur size set karo (e.g., 100x100)
            my_image = ctk.CTkImage(light_image=Image.open(img_path),
                                    dark_image=Image.open(img_path),
                                    size=(100, 100))
            
            # Label ke andar image daalo
            self.logo_image_label = ctk.CTkLabel(self.splash_frame, text="", image=my_image)
            self.logo_image_label.place(relx=0.5, rely=0.35, anchor="center")
            
        except Exception as e:
            print(f"Image Error: {e}")
            # Agar image na mile toh text dikha do
            self.logo_label = ctk.CTkLabel(self.splash_frame, text="SecureCrypt", font=("Impact", 40))
            self.logo_label.place(relx=0.5, rely=0.35, anchor="center")

        # Loading Bar
        self.splash_progress = ctk.CTkProgressBar(self.splash_frame, width=400, mode="indeterminate")
        self.splash_progress.place(relx=0.5, rely=0.6, anchor="center")
        self.splash_progress.start()

        self.status_loading = ctk.CTkLabel(self.splash_frame, text="Loading Assets & Modules...", font=("Arial", 12))
        self.status_loading.place(relx=0.5, rely=0.68, anchor="center")

        self.after(3000, self.load_main_interface)

    def load_main_interface(self):
        self.splash_frame.destroy()
        self.build_ui()

    def build_ui(self):
        # 1. Title
        self.label_title = ctk.CTkLabel(self, text="File Encryption Tool", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        # 2. File Selection
        self.btn_browse = ctk.CTkButton(self, text="Choose File", command=self.browse_file, width=200)
        self.btn_browse.pack(pady=10)
        
        self.label_file = ctk.CTkLabel(self, text="No file selected", text_color="gray")
        self.label_file.pack(pady=5)

        # 3. Password Section (Frame for alignment)
        # Ek transparent frame banaya taaki entry aur button saath rahein
        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent") 
        self.pass_frame.pack(pady=20)

        # Password Entry
        self.entry_pass = ctk.CTkEntry(self.pass_frame, placeholder_text="Enter Password", show="*", width=200)
        self.entry_pass.pack(side="left", padx=(0, 5)) # Right side thoda gap diya

        # Eye Button (👁️)
        self.btn_eye = ctk.CTkButton(self.pass_frame, text="👁️", width=40, command=self.toggle_password)
        self.btn_eye.pack(side="left")
        self.is_password_visible = False # Track karne ke liye ki abhi kya state hai

        # 4. Action Button
        self.btn_run = ctk.CTkButton(self, text="ENCRYPT / DECRYPT", command=self.start_thread, 
                                     width=250, height=50, fg_color="green", hover_color="darkgreen")
        self.btn_run.pack(pady=10)

        # 5. Progress & Status
        self.main_progress = ctk.CTkProgressBar(self, width=300, mode="indeterminate")
        self.main_progress.set(0)

        self.label_status = ctk.CTkLabel(self, text="")
        self.label_status.pack(pady=10)
        self.selected_file_path = ""
    
    def toggle_password(self):
        if self.is_password_visible:
            # Agar dikh raha hai, toh chupa do (*)
            self.entry_pass.configure(show="*")
            self.btn_eye.configure(text="👁️") # Aankh khuli icon
            self.is_password_visible = False
        else:
            # Agar chupa hai, toh dikha do (Text)
            self.entry_pass.configure(show="")
            self.btn_eye.configure(text="❌") # Cross/Close icon taaki user samjhe band karna hai
            self.is_password_visible = True

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.selected_file_path = filename
            self.label_file.configure(text=os.path.basename(filename))

    def start_thread(self):
        password = self.entry_pass.get()
        if not self.selected_file_path or not password:
            self.label_status.configure(text="Error: Missing file or password!", text_color="red")
            return

        self.btn_run.configure(state="disabled", text="Processing...")
        self.main_progress.pack(pady=10)
        self.main_progress.start()
        self.label_status.configure(text="Engine running...", text_color="yellow")
        threading.Thread(target=self.run_process_backend).start()

    def run_process_backend(self):
        password = self.entry_pass.get()
        
        # EXE Path Logic (Using resource_path for consistency)
        base_path = os.getcwd()
        
        # Check standard locations
        possible_paths = [
            os.path.join(base_path, "bin", "encryptor.exe"),        # Dev Mode
            os.path.join(base_path, "dist", "bin", "encryptor.exe"), # Dev Mode (Dist)
            os.path.join(base_path, "bin", "encryptor.exe") # App Mode (Relative)
        ]
        
        exe_path = None
        for p in possible_paths:
            if os.path.exists(p):
                exe_path = p
                break
        
        if not exe_path:
             self.finish_process(False, "Backend (encryptor.exe) not found!")
             return

        try:
            time.sleep(1) 
            subprocess.run([exe_path, self.selected_file_path, password], check=True)
            self.finish_process(True, "Success! Operation Complete.")
        except Exception as e:
            self.finish_process(False, f"Error: {e}")

    def finish_process(self, success, message):
        self.main_progress.stop()
        self.main_progress.pack_forget()
        self.btn_run.configure(state="normal", text="ENCRYPT / DECRYPT")
        color = "green" if success else "red"
        self.label_status.configure(text=message, text_color=color)
        # --- YE NAYA CODE HAI (AUTO CLEAR) ---
        if success:
            # A. Password box ko khaali kar do
            self.entry_pass.delete(0, "end")
            
            # B. Memory se purani file ka path hata do
            self.selected_file_path = ""
            
            # C. Screen par wapas "No file selected" likh do
            self.label_file.configure(text="No file selected")

if __name__ == "__main__":
    app = App()
    app.mainloop()