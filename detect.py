from PIL import Image
import argparse

def extract_hidden_script(image_path):
    image = Image.open(image_path)
    mode = image.mode

    # Handle different image modes
    if mode == 'P':
        image = image.convert('RGB')
        mode = 'RGB'

    pixels = list(image.getdata())
    binary_data = ''

    for pixel in pixels:
        if mode == 'L':
            # Handle grayscale images
            binary_data += str(pixel & 1)
        elif mode in ['RGB', 'RGBA']:
            # Handle color images
            for channel in range(len(pixel)):
                binary_data += str(pixel[channel] & 1)
        else:
            raise ValueError(f"Unsupported image mode: {mode}")

    # Convert binary data to string
    byte_chunks = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ''
    for byte in byte_chunks:
        if len(byte) == 8:  # Ensure we have a full byte
            decoded_message += chr(int(byte, 2))
            # Check for null terminator
            if decoded_message.endswith('\x00\x00\x00\x00\x00\x00\x00\x00'):
                break

    return decoded_message.rstrip('\x00')

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract hidden script from an image.")
    parser.add_argument('input_file', type=str, help="Path to the input image file")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Extract script from the provided image file
    extracted_script = extract_hidden_script(args.input_file)
    print("Extracted script:")
    print(extracted_script)
    
    # Save the extracted script to a .bat file
    output_file = 'extracted_script.bat'
    with open(output_file, 'w') as file:
        file.write(extracted_script)
    print(f"Extracted script saved to {output_file}")

if __name__ == '__main__':
    main()
