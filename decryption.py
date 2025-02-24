import cv2
import json

def decrypt_message():
    # Load the encrypted image
    img = cv2.imread("encrypted_image.png")
    if img is None:
        print("Error: Encrypted image 'encrypted_image.png' not found!")
        return

    # Load metadata
    try:
        with open("metadata.json", "r") as f:
            metadata = json.load(f)
            correct_pass = metadata["password"]
            msg_length = metadata["msg_length"]
    except FileNotFoundError:
        print("Error: Metadata file not found! The image may not have been properly encrypted.")
        return
    except json.JSONDecodeError:
        print("Error: Metadata file is corrupted!")
        return
    except KeyError:
        print("Error: Metadata file is missing required information!")
        return

    # Ask user for the decryption passcode
    password = input("Enter passcode for decryption: ").strip()
    if password != correct_pass:
        print("Error: Incorrect passcode. Access denied!")
        return

    message = ""
    n = 0  # row index
    m = 0  # column index
    z = 0  # channel index

    # Read the embedded message from the image
    try:
        for i in range(msg_length):
            message += chr(img[n, m, z])
            n += 1
            m += 1
            z = (z + 1) % 3
        
        print("\nDecrypted message:", message)
    except Exception as e:
        print(f"Error during decryption: {e}")

if __name__ == "__main__":
    decrypt_message()
