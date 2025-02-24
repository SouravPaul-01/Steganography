import cv2
import os
import json

def encrypt_message():
    # Load cover image
    img = cv2.imread("mypic.jpg")
    if img is None:
        print("Error: Cover image 'mypic.jpg' not found!")
        return

    # Input secret message and password
    msg = input("Enter secret message: ").strip()
    if not msg:
        print("Error: Message cannot be empty!")
        return
    
    password = input("Enter a passcode: ").strip()
    if not password:
        print("Error: Password cannot be empty!")
        return

    # Save the password and message length to a metadata file
    metadata = {
        "password": password,
        "msg_length": len(msg)
    }
    
    try:
        with open("metadata.json", "w") as f:
            json.dump(metadata, f)
    except Exception as e:
        print(f"Error saving metadata: {e}")
        return

    # Calculate maximum possible message length
    max_chars = (img.shape[0] * img.shape[1] * 3) // 3  # Each char needs 1 channel
    if len(msg) > max_chars:
        print(f"Error: Message too long! Maximum length is {max_chars} characters")
        return

    # Embed the message into the image
    n = 0  # row index
    m = 0  # column index
    z = 0  # channel index (0=Blue, 1=Green, 2=Red in OpenCV)

    # Create a copy of the image to avoid modifying the original
    encrypted_img = img.copy()

    for char in msg:
        encrypted_img[n, m, z] = ord(char)
        n += 1
        m += 1
        z = (z + 1) % 3

    # Save the encrypted image
    try:
        cv2.imwrite("encrypted_image.png", encrypted_img)
        print("Message successfully embedded into encrypted_image.png!")
        
        # Open the image (platform-independent)
        if os.name == 'nt':  # Windows
            os.system("start encrypted_image.png")
        elif os.name == 'posix':  # macOS/Linux
            os.system("open encrypted_image.png" if os.uname().sysname == 'Darwin' else "xdg-open encrypted_image.png")
    except Exception as e:
        print(f"Error saving encrypted image: {e}")

if __name__ == "__main__":
    encrypt_message()
