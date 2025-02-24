import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import json
import os
from PIL import Image, ImageTk

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography Tool")
        self.root.geometry("1000x700")
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')  # or 'alt', 'default', 'classic'
        
        # Configure styles
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Action.TButton', font=('Helvetica', 10), padding=10)
        
        # Main container with padding
        main_container = ttk.Frame(root, padding="20")
        main_container.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(
            main_container, 
            text="Image Steganography", 
            style='Title.TLabel'
        )
        title_label.pack(pady=20)

        # Variables
        self.cover_image_path = tk.StringVar()
        self.encrypted_image_path = tk.StringVar()
        self.password = tk.StringVar()
        self.message = tk.StringVar()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill='both')

        # Create tabs with padding
        self.encrypt_tab = ttk.Frame(self.notebook, padding="10")
        self.decrypt_tab = ttk.Frame(self.notebook, padding="10")
        
        self.notebook.add(self.encrypt_tab, text='✉️ Encrypt Message')
        self.notebook.add(self.decrypt_tab, text='🔓 Decrypt Message')

        self.setup_encrypt_tab()
        self.setup_decrypt_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_container, 
            textvariable=self.status_var,
            relief='sunken',
            padding=5
        )
        status_bar.pack(fill='x', pady=(10,0))

    def setup_encrypt_tab(self):
        # Create main containers
        left_frame = ttk.Frame(self.encrypt_tab)
        right_frame = ttk.Frame(self.encrypt_tab)
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        right_frame.pack(side='right', fill='both', expand=True, padx=10)

        # Image preview section
        preview_frame = ttk.LabelFrame(
            left_frame, 
            text="Image Preview",
            padding="10"
        )
        preview_frame.pack(fill='both', expand=True)
        
        self.preview_label = ttk.Label(preview_frame)
        self.preview_label.pack(padx=10, pady=10)

        # No image selected label
        ttk.Label(
            preview_frame,
            text="No image selected",
            style='Header.TLabel'
        ).pack()

        # Input section
        input_frame = ttk.LabelFrame(
            right_frame,
            text="Encryption Settings",
            padding="10"
        )
        input_frame.pack(fill='both', expand=True)

        # Select image button
        ttk.Button(
            input_frame,
            text="🖼️ Select Cover Image",
            command=self.select_cover_image,
            style='Action.TButton'
        ).pack(fill='x', pady=10)

        # Message input
        ttk.Label(
            input_frame,
            text="Secret Message:",
            style='Header.TLabel'
        ).pack(pady=(10,5))
        
        self.message_text = tk.Text(
            input_frame,
            height=4,
            width=30,
            font=('Helvetica', 10),
            wrap='word'
        )
        self.message_text.pack(fill='x', pady=(0,10))

        # Password input
        ttk.Label(
            input_frame,
            text="Password:",
            style='Header.TLabel'
        ).pack(pady=(10,5))
        
        password_entry = ttk.Entry(
            input_frame,
            textvariable=self.password,
            show="•",
            font=('Helvetica', 10)
        )
        password_entry.pack(fill='x', pady=(0,20))

        # Encrypt button
        ttk.Button(
            input_frame,
            text="🔒 Encrypt and Save",
            command=self.encrypt_message,
            style='Action.TButton'
        ).pack(fill='x', pady=10)

    def setup_decrypt_tab(self):
        # Main container
        decrypt_frame = ttk.LabelFrame(
            self.decrypt_tab,
            text="Message Decryption",
            padding="20"
        )
        decrypt_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Select encrypted image button
        ttk.Button(
            decrypt_frame,
            text="🔍 Select Encrypted Image",
            command=self.select_encrypted_image,
            style='Action.TButton'
        ).pack(fill='x', pady=20)

        # Password input
        ttk.Label(
            decrypt_frame,
            text="Enter Password:",
            style='Header.TLabel'
        ).pack(pady=(10,5))
        
        ttk.Entry(
            decrypt_frame,
            textvariable=self.password,
            show="•",
            font=('Helvetica', 10)
        ).pack(fill='x', pady=(0,20))

        # Decrypt button
        ttk.Button(
            decrypt_frame,
            text="🔓 Decrypt Message",
            command=self.decrypt_message,
            style='Action.TButton'
        ).pack(fill='x', pady=20)

        # Decrypted message display
        ttk.Label(
            decrypt_frame,
            text="Decrypted Message:",
            style='Header.TLabel'
        ).pack(pady=(20,5))
        
        self.decrypted_text = tk.Text(
            decrypt_frame,
            height=6,
            width=50,
            font=('Helvetica', 10),
            wrap='word',
            state='disabled'
        )
        self.decrypted_text.pack(pady=(0,20))

    def select_cover_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")],
            initialdir="./images"
        )
        if file_path:
            self.cover_image_path.set(file_path)
            self.show_preview(file_path)
            self.status_var.set(f"Selected: {os.path.basename(file_path)}")

    def select_encrypted_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Encrypted Image",
            filetypes=[("PNG files", "*.png")],
            initialdir="./images/encrypted"
        )
        if file_path:
            self.encrypted_image_path.set(file_path)
            self.status_var.set(f"Selected: {os.path.basename(file_path)}")

    def show_preview(self, image_path):
        try:
            # Load and resize image for preview
            image = Image.open(image_path)
            # Calculate aspect ratio
            aspect_ratio = image.width / image.height
            # Set maximum dimensions
            max_size = (300, 300)
            
            # Calculate new size maintaining aspect ratio
            if aspect_ratio > 1:
                new_size = (max_size[0], int(max_size[1] / aspect_ratio))
            else:
                new_size = (int(max_size[0] * aspect_ratio), max_size[1])
                
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image preview: {str(e)}")

    def encrypt_message(self):
        try:
            if not self.cover_image_path.get():
                messagebox.showerror("Error", "Please select a cover image first!")
                return

            msg = self.message_text.get("1.0", tk.END).strip()
            if not msg:
                messagebox.showerror("Error", "Please enter a message to encrypt!")
                return

            if not self.password.get():
                messagebox.showerror("Error", "Please enter a password!")
                return

            self.status_var.set("Encrypting message...")
            self.root.update()

            # Load cover image
            img = cv2.imread(self.cover_image_path.get())
            
            # Calculate maximum possible message length
            max_chars = (img.shape[0] * img.shape[1] * 3) // 3
            if len(msg) > max_chars:
                messagebox.showerror("Error", 
                    f"Message too long! Maximum length is {max_chars} characters")
                return

            # Save metadata
            metadata = {
                "password": self.password.get(),
                "msg_length": len(msg)
            }

            # Get save location
            os.makedirs("./images/encrypted", exist_ok=True)
            save_path = filedialog.asksaveasfilename(
                title="Save Encrypted Image",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialdir="./images/encrypted"
            )
            
            if not save_path:
                self.status_var.set("Encryption cancelled")
                return

            # Save metadata alongside the image
            metadata_path = os.path.splitext(save_path)[0] + "_metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f)

            # Embed message
            encrypted_img = img.copy()
            n, m, z = 0, 0, 0
            for char in msg:
                encrypted_img[n, m, z] = ord(char)
                n += 1
                m += 1
                z = (z + 1) % 3

            # Save encrypted image
            cv2.imwrite(save_path, encrypted_img)
            self.status_var.set("Message encrypted successfully!")
            messagebox.showinfo("Success", "Message encrypted successfully!")

        except Exception as e:
            self.status_var.set("Encryption failed!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def decrypt_message(self):
        try:
            if not self.encrypted_image_path.get():
                messagebox.showerror("Error", "Please select an encrypted image first!")
                return

            self.status_var.set("Decrypting message...")
            self.root.update()

            # Load encrypted image
            img = cv2.imread(self.encrypted_image_path.get())
            
            # Load metadata
            metadata_path = os.path.splitext(self.encrypted_image_path.get())[0] + "_metadata.json"
            with open(metadata_path, "r") as f:
                metadata = json.load(f)

            if self.password.get() != metadata["password"]:
                self.status_var.set("Incorrect password!")
                messagebox.showerror("Error", "Incorrect password!")
                return

            # Decrypt message
            message = ""
            n, m, z = 0, 0, 0
            for i in range(metadata["msg_length"]):
                message += chr(img[n, m, z])
                n += 1
                m += 1
                z = (z + 1) % 3

            # Display decrypted message
            self.decrypted_text.configure(state='normal')
            self.decrypted_text.delete("1.0", tk.END)
            self.decrypted_text.insert("1.0", message)
            self.decrypted_text.configure(state='disabled')
            
            self.status_var.set("Message decrypted successfully!")

        except FileNotFoundError:
            self.status_var.set("Metadata file not found!")
            messagebox.showerror("Error", "Metadata file not found!")
        except Exception as e:
            self.status_var.set("Decryption failed!")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Steganography Tool")
    
    # Set window icon (if you have one)
    # root.iconbitmap('path/to/icon.ico')
    
    # Set minimum window size
    root.minsize(1000, 700)
    
    # Center window on screen
    window_width = 1000
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = SteganographyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 