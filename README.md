# Image Steganography Project

A simple yet secure implementation of text hiding within images using steganography techniques. This project allows users to embed secret messages into images and later decrypt them using a password.

## 📋 Features

- Embed text messages into images
- Password protection for message security
- Support for any PNG/JPG images as cover
- Platform-independent (Windows, macOS, Linux)
- Automatic message length tracking
- Error handling and validation
- Non-destructive to original images

## 🔧 Requirements

- Python 3.6+
- OpenCV (cv2)
- Pillow (PIL)
- tkinter (usually comes with Python)
- A cover image file

## 📦 Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install opencv-python
   pip install Pillow
   ```
3. Place your cover image in the project directory as "mypic.jpg"

## 🚀 Usage

### Using the GUI (Recommended for new users)

Run the GUI version:
```bash
python stego_gui.py
```

1. Select the "Encrypt Message" tab to hide a message:
   - Click "Select Cover Image" to choose your image
   - Enter your secret message
   - Set a password
   - Click "Encrypt and Save" to save the encrypted image

2. Select the "Decrypt Message" tab to reveal a message:
   - Click "Select Encrypted Image" to choose the encrypted image
   - Enter the password
   - Click "Decrypt Message" to reveal the hidden message

### Encrypting a Message (Command Line)

1. Place your cover image in the project directory and name it "mypic.jpg"
2. Run the encryption script:
   ```bash
   python encryption.py
   ```
3. Follow the prompts:
   - Enter your secret message
   - Create a password
4. The encrypted image will be saved as "encrypted_image.png"

### Decrypting a Message

1. Ensure you have the encrypted image ("encrypted_image.png")
2. Run the decryption script:
   ```bash
   python decryption.py
   ```
3. Enter the password when prompted
4. The secret message will be displayed

## 📁 Project Structure

```
steganography_project/
│
├── src/
│   ├── encryption.py      # Script for embedding messages
│   ├── decryption.py      # Script for extracting messages
│   └── stego_gui.py       # GUI application
│
├── README.md             # Project documentation
├── requirements.txt      # Package dependencies
└── images/              # Directory for your images
    ├── mypic.jpg        # Your cover image (you provide this)
    └── encrypted/       # Directory for encrypted images
```

When using the program:
- Place your cover images in the `images/` directory
- Encrypted images will be saved in `images/encrypted/`
- Metadata files will be stored alongside encrypted images

## ⚠️ Important Notes

1. The maximum message length depends on your cover image size
2. Always use PNG format for encrypted images to avoid data loss
3. Keep the metadata.json file with your encrypted image
4. Don't modify the encrypted image or it may corrupt the message
5. Remember your password - it cannot be recovered

## 🔒 Security Considerations

- The message is embedded using basic pixel manipulation
- Security relies on password protection
- Don't share the metadata.json file with others
- Use strong passwords for better security

## ⚡ Limitations

- Cover image must be larger than your message
- Only supports text messages
- Encrypted image must be saved as PNG
- No compression support
- Password is stored in metadata file

## 🐛 Troubleshooting

1. "Cover image not found":
   - Ensure "mypic.jpg" exists in the project directory

2. "Message too long":
   - Use a larger cover image
   - Reduce message length

3. "Metadata file not found":
   - Keep metadata.json in the same directory as the scripts

4. "Incorrect password":
   - Double-check your password
   - Ensure metadata.json hasn't been modified

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements. 