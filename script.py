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

    # Máscara para remover el fondo
    mask = labels.reshape(img.shape[:2])
    background = (mask == 0)

    # Combinar el primer plano con el fondo blanco
    img_with_white_bg = white_background.copy()
    img_with_white_bg[~background] = img[~background]

    # Guardar las imágenes
    cv2.imwrite("original_image.png", img)
    cv2.imwrite("segmented_image.png", segmented_image)
    cv2.imwrite("image_with_white_background.png", img_with_white_bg)

# Probar la función
remove_background('./test_images/one_sparkplug.jpeg', './test_images/white_background.jpg')