from PIL import Image
import binascii

def string_to_binary(text):
    binary_text = ''.join(format(ord(char), '08b') for char in text)
    return binary_text

def embed_bat_script(image_path, output_path, script_content):
    binary_script = string_to_binary(script_content) + '00000000'  # Append null terminator
    image = Image.open(image_path)
    mode = image.mode
    size = image.size

    print(f"Original image mode: {mode}")  # Diagnostic print statement

    # Convert image to RGB if it is in paletted mode
    if mode == 'P':
        image = image.convert('RGB')
        mode = 'RGB'

    pixels = list(image.getdata())

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        if mode == 'L':
            # Handle grayscale images
            new_pixel = [pixel]
        elif mode == 'RGB':
            # Handle RGB images
            new_pixel = list(pixel[:3])
        elif mode == 'RGBA':
            # Handle RGBA images
            new_pixel = list(pixel[:3])
        else:
            raise ValueError(f"Unsupported image mode: {mode}")

        # Modify pixel values
        for channel in range(len(new_pixel)):
            if bit_index < len(binary_script):
                new_pixel[channel] = (new_pixel[channel] & ~1) | int(binary_script[bit_index])
                bit_index += 1

        # Ensure we are appending a tuple
        new_pixels.append(tuple(new_pixel))

    # Create new image with appropriate mode
    new_image = Image.new(mode, size)
    new_image.putdata(new_pixels)
    new_image.save(output_path)

# Example usage
bat_script_content = "@echo off\necho Hello, it's Steganographed!\npause\n"
embed_bat_script('nike.png', 'nike_bat.png', bat_script_content)
