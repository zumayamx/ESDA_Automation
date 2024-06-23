import cv2 as cv

def add_measurements(image):
    # Read the image such as was taken by the camera
    image = cv.imread(image)
    return image