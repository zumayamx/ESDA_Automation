# TO DO:
# - CENTER THE IMAGE IN A STATIC IMAGE TO ADD MEASUREMENTS
# - REQUEST THE MEASUREMENTS TO ADD

import cv2
import numpy as np
import matplotlib.pyplot as plt

def remove_noise(image_path):
        # Leer la imagen
    img = cv2.imread(image_path)
    if img is None:
        print("Error: could not read image.")
        return

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un umbral para segmentar la bujía del fondo
    _, binary = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY_INV)

    # Aplicar operaciones morfológicas para eliminar el ruido
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Crear una máscara para la bujía
    mask = closing

    # Aplicar la máscara a la imagen original
    result = cv2.bitwise_and(img, img, mask=mask)

    # Mostrar los resultados
    # plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('Original')
    # plt.subplot(1, 3, 2), plt.imshow(mask, cmap='gray'), plt.title('Mask')
    # plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)), plt.title('Result')
    # plt.show()

    # Guardar la imagen resultante
    cv2.imwrite("cleaned_image.png", result)

def segment_with_grabcut(image_path):
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], np.uint8)
    
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    rect = (50, 50, img.shape[1]-50, img.shape[0]-50) # Define el rectángulo inicial
    
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = img * mask2[:, :, np.newaxis]
    
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

# Probar la función
# segment_with_grabcut('./test_images/sparkplugs.jpeg')

# Probar la función
# remove_noise('./test_images/one_sparkplug.jpeg')
remove_noise('./test_images/sparkplugs.jpeg')