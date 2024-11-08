import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils

def getVertices(image_path):
    # Lee la imagen
    img = cv2.imread(image_path)
    cv2.imshow('Original Image', img)
    
    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Aplica un suavizado (blur) para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplica un umbral adaptativo para destacar el objeto sobre el fondo
    _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Aplica operaciones morfológicas para limpiar posibles imperfecciones
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Muestra la imagen final en blanco y negro
    cv2.imshow("Thresholded Image", cleaned)
    
    # Buscar el vertice más largo en la imagen limpia
    cnts = cv2.findContours(cleaned.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    
    output = img.copy()
    cv2.drawContours(output, [c], -1, (0, 0, 255), 3)
    (x, y, w, h) = cv2.boundingRect(c)
    text = "original, num_pts={}".format(len(c))
    cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX,
        0.9, (0, 255, 0), 2)
    # show the original contour image
    print("[INFO] {}".format(text))
    cv2.imshow("Original Contour", output)
    
    # contour approximation
    for eps in np.linspace(0.001, 0.05, 10):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, eps * peri, True)
        
        output = img.copy()
        cv2.drawContours(output, [approx], -1, (255, 0, 0), 3)
        
        text = "eps={:.4f}, num_pts={}".format(eps, len(approx))
        cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (0, 255, 0), 2)
        # show the approximated contour image
        print("[INFO] {}".format(text))
        cv2.imshow("Approximated Contour", output)
        cv2.waitKey(0)

# Llama a la función con la ruta de la imagen
getVertices('centered_image.png')