import cv2
import os
import string
import numpy as np

def encode_message():
    # Load the image
    image_path = input("Enter the path to the image: ")
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Image not found. Please check the path.")
            return
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    # Get secret message and password
    msg = input("Enter secret message: ")
    password = input("Enter a passcode: ")
    
    # Check if the message can fit in the image
    height, width, channels = img.shape
    max_bytes = height * width * channels // 8  # Each pixel component can store 1 bit
    
    if len(msg) > max_bytes:
        print(f"Message too long for this image. Maximum length: {max_bytes} characters")
        return
    
    # Create a copy of the image to avoid modifying the original
    stego_img = img.copy()
    
    # Encode message length first (for decoding)
    msg_len = len(msg)
    
    # Store message in the image (1 character per pixel)
    n, m, z = 0, 0, 0
    
    # Store message length in first pixel
    stego_img[0, 0, 0] = msg_len // 255
    stego_img[0, 0, 1] = msg_len % 255
    
    # Store actual message
    for i in range(len(msg)):
        # Get the ASCII value of the character
        char_value = ord(msg[i])
        
        # Store the value in the image
        stego_img[n, m, z] = char_value
        
        # Move to next position
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m >= width:
                m = 0
                n += 1
                if n >= height:
                    print("Warning: Message exceeds image capacity")
                    break
    
    # Save the image with hidden message
    output_path = "encryptedImage.jpg"
    cv2.imwrite(output_path, stego_img)
    print(f"Message hidden successfully in {output_path}")
    
    # Store password in a separate file (not secure, just for demonstration)
    with open("password.txt", "w") as f:
        f.write(password)
    
    # Open the image
    try:
        os.system(f"start {output_path}")  # For Windows
    except:
        print(f"Image saved as {output_path}")

def decode_message():
    # Load the image with hidden message
    image_path = input("Enter the path to the encrypted image: ")
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("Image not found. Please check the path.")
            return
    except Exception as e:
        print(f"Error loading image: {e}")
        return
    
    # Get password
    password = input("Enter passcode for decryption: ")
    
    # Check password (in a real application, use a more secure method)
    try:
        with open("password.txt", "r") as f:
            stored_password = f.read()
        
        if password != stored_password:
            print("YOU ARE NOT AUTHORIZED")
            return
    except:
        print("Password file not found")
        return
    
    # Get message length from first pixel
    msg_len_high = img[0, 0, 0]
    msg_len_low = img[0, 0, 1]
    msg_len = msg_len_high * 255 + msg_len_low
    
    # Extract message
    message = ""
    n, m, z = 0, 0, 0
    
    # Skip the pixel used for length storage
    z = 2
    
    # Extract each character
    for i in range(msg_len):
        # Get the ASCII value from the image
        char_value = img[n, m, z]
        
        # Convert ASCII to character and add to message
        message += chr(char_value)
        
        # Move to next position
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m >= img.shape[1]:
                m = 0
                n += 1
    
    print("Decrypted message:", message)

def main():
    while True:
        print("\nImage Steganography")
        print("1. Encode a message in an image")
        print("2. Decode a message from an image")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '1':
            encode_message()
        elif choice == '2':
            decode_message()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
