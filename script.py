# TO DO:
# - VERIFY THE SIZE OF THE OBJECT AND THE BACKGROUND -- **SO IMPORTANT**
# - TO HAVE MANU FUNCTIONS TO DO DIFFERENT THINGS, NOT ONLY ADD MEASUREMENTS
# - CHECK THE DIFF SHAPES OF THE OBJECTS
# - REM THE CONTOURS OF THE OBJECTS
import cv2

import numpy as np
import rembg
# import numpy as np
# import matplotlib.pyplot as plt
from PIL import Image

def get_dimensions_of_any_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return
    
    # Get the dimensions of the image
    height, width, channels = img.shape
    print("Height:", height)
    print("Width:", width)
    print("Channels:", channels)

def get_edges_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: could not read image at ged_edges_image.")
        return
    
    # Convert the image to grayscale
    gray_test_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect edges in the image using the Canny
    edges_image = cv2.Canny(gray_test_img, 50, 150)

    # Show the image with edges, like return?
    cv2.imwrite("edges_image.png", edges_image)

def find_first_white_pixel(image_path):
    #Read the image
    img = Image.open(image_path)

    if img is None:
        print("Error: could not read image at find_first_white_pixel.")
        return

    # Convert image to RGB
    edges_image = img.convert("RGB")
    
    # cv2.imwrite("edges_image_image_color.png", edges_image)
    pixels = edges_image.load()

    # Get the dimensions of the image
    width, height = edges_image.size

    # Find the first white pixel from right to left
    pixel_right_left = None
    for x in range(width - 1, -1, -1):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                pixel_right_left = x
                break
        if pixel_right_left is not None:
            break
    
    # Find the first white pixel from the left to right
    pixel_left_right = None
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                pixel_left_right = x
                break
        if pixel_left_right is not None:
            break
    
    # Find the first white pixel from top to bottom
    pixel_top_bottom = None
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                pixel_top_bottom = y
                break
        if pixel_top_bottom is not None:
            break
    
    # Find the first white pixel from bottom to top
    pixel_bottom_top = None
    for y in range(height - 1, -1, -1):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                pixel_bottom_top = y
                break
        if pixel_bottom_top is not None:
            break
    
    return pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top

# This funcion is to see what is the position of the object in the image, it's not used in a real case
def draw_red_lines(pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top, image_path):
    # Read the image with PIL
    img = Image.open(image_path)

    if img is None:
        print("Error: could not read image at draw_red_lines.")
        return

    # Convert image to RGB
    edges_image = img.convert("RGB")

    # Convert image to pixels read format
    pixels = edges_image.load()

    # Get the dimensions of the image
    width, height = edges_image.size

    # Draw a horizontal red line at the found position
    if pixel_top_bottom and pixel_bottom_top is not None:
        for x in range(width):
            pixels[x, pixel_top_bottom - 1] = (255, 0, 0)
            pixels[x, pixel_bottom_top + 1] = (255, 0, 0)

    # Draw a vertical red line at the found position
    if pixel_right_left and pixel_left_right is not None:
        for y in range(height):
            pixels[pixel_right_left + 1, y] = (255, 0, 0)
            pixels[pixel_left_right - 1, y] = (255, 0, 0)

    # Save the modified image, like return?
    edges_image.save("edges_image_with_line_red_in_pixel.png")

def paste_object_image_in_white_background(pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top, white_image_path, object_image_path):
    # Read the white background and the object image
    white_background = cv2.imread(white_image_path)
    obj_img = cv2.imread(object_image_path)
    
    # Crop the object image based on the provided coordinates
    cropped_image = obj_img[pixel_top_bottom:pixel_bottom_top, pixel_left_right:pixel_right_left]

    # Get dimensions of the cropped image and the white background
    height, width, _ = cropped_image.shape
    height_white, width_white, _ = white_background.shape

    # Validate if the white background is large enough to contain the cropped image
    if height > height_white or width > width_white:
        # Option 1: Automatically resize the white background
        # Calculate the new dimensions for the white background to ensure it fits the cropped image
        new_height = max(height + 300, height_white)
        new_width = max(width + 300, width_white)
        white_background = cv2.resize(white_background, (new_width, new_height))

        # Update the dimensions after resizing
        height_white, width_white, _ = white_background.shape
        print(f"Resized white background to: {new_width}x{new_height}")

    # Find the position to paste the cropped image in the white background
    y_position = (height_white - height) // 2
    x_position = (width_white - width) // 2

    # Paste the cropped image in the white background
    white_background[y_position:y_position + height, x_position:x_position + width] = cropped_image

    # Save the image with the object centered in the white background
    cv2.imwrite("centered_image.png", white_background)

    return y_position, x_position, height, width

def draw_accurate_lines_meansurements(y_position, x_position, h, w,  image_path):

    #Read the image for drawing the measurements
    img = Image.open(image_path)
    img_centered_edges = img.convert("RGB")
    pixels_centered = img_centered_edges.load()

    # Get the dimensions of the image
    height, width = h, w

    y_position_r = y_position - 80

    for x in range (x_position, x_position + width + 1):
        for r in range (5, -1, -1):
            pixels_centered[x, y_position_r  - r] = (0, 0, 0)

    x_position_r = x_position - 80

    for y in range(y_position, y_position + height + 1):
        for r in range (5, -1, -1):
            pixels_centered[x_position_r - r, y] = (0, 0, 0)

    print("y_position_r: ", y_position_r)
    print("x_position_r: ", x_position_r)

    print("y_position: ", y_position)
    print("x_position: ", x_position)

    # Draw the remaining line in x axis left
    for x in range (x_position - 5, x_position):
        for r in range (y_position_r + 5, y_position_r - 11, -1):
            pixels_centered[x, r] = (0, 0, 0)
    
    # Draw the remaining line in x axis right
    for x in range (x_position + width + 1, x_position + width + 6):
        for r in range (y_position_r + 5, y_position_r - 11, -1):
            pixels_centered[x, r] = (0, 0, 0)

    # Draw the remaining line in y axis top
    for y in range (y_position - 5, y_position):
        for r in range (x_position_r + 5, x_position_r - 11, -1):
            pixels_centered[r, y] = (0, 0, 0)
    
    # Draw the remaining line in y axis bottom
    for y in range (y_position + height + 1, y_position + height + 6):
        for r in range (x_position_r + 5, x_position_r - 11, -1):
            pixels_centered[r, y] = (0, 0, 0)
    
    img_centered_edges.save("centered_image_with_line.png")

    # Read the image for drawing the measurements
    img_measuremets = cv2.imread("centered_image_with_line.png")
    if img_measuremets is None:
        print("Error: could not read image.")
        return
    
    height_input = input("Enter the heigh of the object: ")
    width_input = input("Enter the width of the object: ")
    font = cv2.FONT_HERSHEY_SIMPLEX

    position_with = (x_position + (int(width) // 2) - 40, y_position_r - 40)
    position_height = (x_position_r - 150, y_position + (int(height) // 2) + 5)

    cv2.putText(img_measuremets, f'{width_input} cm', position_with, font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_measuremets, f'{height_input} cm', position_height, font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.imwrite("centered_image_with_line_and_measurements.png", img_measuremets)

    get_dimensions_of_any_image("centered_image_with_line.png")

def try_to_remove_background(image_path, white_image_path):
    input_image = Image.open(image_path)
    input_array = np.array(input_image)
    output_array = rembg.remove(input_array)

    print("image")
    output_image = Image.fromarray(output_array)

    # Mantener output_image en RGBA para la transparencia
    if output_image.mode != 'RGBA':
        output_image = output_image.convert('RGBA')
    
    # Abrir la imagen de fondo blanco
    white_image = Image.open(white_image_path)

    # Asegurar que la imagen de fondo blanco tenga el mismo tamaño que la imagen de entrada
    white_image = white_image.resize(output_image.size)
    
    # Pegar la imagen con transparencia sobre el fondo blanco
    white_image.paste(output_image, (0, 0), output_image)

    # Convertir a RGB antes de guardar
    white_image = white_image.convert('RGB')
    white_image.save("rem_bujia_noise_white.jpg")

    print("save")
    output_image.convert('RGB').save("rem_bujia_noise.jpg")
    print("saved")

def main():

    # Path of the general image test_images/bujia_rm-removebg-preview.jpg
    image_path = "rem_bujia_noise_white.jpg"
    
    # Path of the white background image
    white_image_path = "./test_images/white_background.jpg"

    example_image = "IMG_1317.png"

    try_to_remove_background(example_image, white_image_path)
    # Get the dimensions of the image
    get_dimensions_of_any_image(image_path)

    # Ged dimensions of white background
    get_dimensions_of_any_image(white_image_path)

    # Get the edges of the image
    get_edges_image(image_path)

    # Find the first white pixel in the image
    pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top = find_first_white_pixel("edges_image.png")

    # Draw red lines in the image
    draw_red_lines(pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top, "edges_image.png")

    # Paste the object image in a white background
    y_position, x_position, heigh, width = paste_object_image_in_white_background(pixel_right_left, pixel_left_right, pixel_top_bottom, pixel_bottom_top, white_image_path, image_path)

    # Draw the accurate lines for measurements
    draw_accurate_lines_meansurements(y_position, x_position, heigh, width, "centered_image.png")

if __name__ == "__main__":
    main()
