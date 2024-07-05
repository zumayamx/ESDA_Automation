#TO DO:
# - CENTER THE IMAGE IN A STATIC IMAGE TO ADD MEASUREMENTS
# - REQUEST THE MEASUREMENTS TO ADD

import cv2
import numpy as np

def remove_background(image_path, white_background_path):
    # Leer la imagen
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return

    # Leer la imagen de fondo blanco
    white_background = cv2.imread(white_background_path)
    if white_background is None:
        print("Error: could not read white background image.")
        return

    # Cambiar el tamaño de la imagen de fondo blanco para que coincida con la imagen original
    white_background = cv2.resize(white_background, (img.shape[1], img.shape[0]))

    # Convertir la imagen a RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Remodelar la imagen a un arreglo 2D de píxeles y 3 valores de color (RGB)
    pixel_values = img_rgb.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Definir criterios para k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    k = 2  # Número de clusters (fondo y primer plano)
    _, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convertir los centros a valores de 8 bits
    centers = np.uint8(centers)

    # Aplanar el arreglo de etiquetas
    labels = labels.flatten()

    # Convertir todos los píxeles al color de los centroides
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(img.shape)

    # Guardar la imagen segmentada
    cv2.imwrite("segmented_image.png", segmented_image)

    # Usar la imagen segmentada para crear una máscara más precisa
    gray_segmented = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2GRAY)
    _, mask = cv2.threshold(gray_segmented, 1, 255, cv2.THRESH_BINARY)

    # Invertir la máscara para obtener el fondo
    mask_inv = cv2.bitwise_not(mask)

    # Crear una imagen de fondo blanco del mismo tamaño
    white_background = np.full_like(img, 255)

    # Aplicar la máscara para obtener la imagen con fondo blanco
    img_with_white_bg = cv2.bitwise_and(img, img, mask=mask)
    white_bg_part = cv2.bitwise_and(white_background, white_background, mask=mask_inv)
    result = cv2.add(img_with_white_bg, white_bg_part)

    # Guardar la imagen final con fondo blanco
    cv2.imwrite("image_with_white_background.png", result)

# Probar la función
remove_background('./test_images/bujias.jpg', './test_images/white_background.jpg')