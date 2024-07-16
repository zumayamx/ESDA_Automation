# TO DO:
# - CENTER THE IMAGE IN A STATIC IMAGE TO ADD MEASUREMENTS
# - REQUEST THE MEASUREMENTS TO ADD
# - LEAVE THE FUNCTION TO REMOVE NOISE
# - FOCUS ON THE FUCTION TO CENTER THE OBJECT IN A STATIC IMAGE

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def center_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return
    
    # Convert the image to grayscale
    gray_test_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect edges in the image using the Canny
    edges = cv2.Canny(gray_test_img, 50, 150)

    # Show the image with edges
    cv2.imwrite("edges_image.png", edges)

    # Open the image with PIL
    image_path = "edges_image.png"
    edges = Image.open(image_path)

    # Convert image to RGB
    edges = edges.convert("RGB")
    pixels = edges.load()

    width, height = edges.size
    print("Height of edge image:", height)
    print("Width of edge image:", width)

    # Find the first white pixel from right to left
    line_x = None
    for x in range(width - 1, -1, -1):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                line_x = x
                break
        if line_x is not None:
            break
    
    # Find the first white pixel from the left to right
    line_x_left = None
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                line_x_left = x
                break
        if line_x_left is not None:
            break
    
    # Find the first white pixel from top to bottom
    line_y = None
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                line_y = y
                break
        if line_y is not None:
            break
    
    # Find the first white pixel from bottom to top
    line_y_top = None
    for y in range(height - 1, -1, -1):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r > 200 and g > 200 and b > 200:  # Considering near white pixel
                line_y_top = y
                break
        if line_y_top is not None:
            break

    # Draw a horizontal red line at the found position
    if line_y is not None:
        for x in range(width):
            pixels[x, line_y] = (255, 0, 0)
            pixels[x, line_y_top] = (255, 0, 0)

    # Draw a vertical red line at the found position
    if line_x is not None and line_x_left is not None:
        for y in range(height):
            pixels[line_x, y] = (255, 0, 0)
            pixels[line_x_left, y] = (255, 0, 0)

    # Save the modified image
    edges.save("edges_image_with_line_in_pixel.png")


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

# Test fuctions
print("Dimensions of background image: ")
get_dimensions_of_any_image('./test_images/white_background.jpg')
print("Dimensions of test image: ")
get_dimensions_of_any_image('./test_images/one_sparkplug_clean.jpeg')
center_image('./test_images/one_sparkplug_clean.jpeg')

# def remove_noise(image_path):
#         # Leer la imagen
#     img = cv2.imread(image_path)
#     if img is None:
#         print("Error: could not read image.")
#         return

#     # Convertir la imagen a escala de grises
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Aplicar un umbral para segmentar la bujía del fondo
#     _, binary = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)

#     # Aplicar operaciones morfológicas para eliminar el ruido
#     kernel = np.ones((3, 3), np.uint8)
#     opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
#     closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # Crear una máscara para la bujía
#     mask = closing

#     # Aplicar la máscara a la imagen original
#     result = cv2.bitwise_and(img, img, mask=mask)

#     # Guardar la imagen resultante
#     cv2.imwrite("cleaned_image.png", result)

#     # Centrar la imagen en un fondo blanco

# remove_noise('./test_images/box_sparkplug.jpeg')

# def segment_with_grabcut(image_path):
#     img = cv2.imread(image_path)
#     mask = np.zeros(img.shape[:2], np.uint8)
    
#     bgdModel = np.zeros((1, 65), np.float64)
#     fgdModel = np.zeros((1, 65), np.float64)
    
#     rect = (50, 50, img.shape[1]-50, img.shape[0]-50) # Define el rectángulo inicial
    
#     cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
#     mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
#     img = img * mask2[:, :, np.newaxis]
    
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.axis('off')
#     plt.show()

# Probar la función
# segment_with_grabcut('./test_images/sparkplugs.jpeg')

# Probar la función
# remove_noise('./test_images/one_sparkplug.jpeg')
