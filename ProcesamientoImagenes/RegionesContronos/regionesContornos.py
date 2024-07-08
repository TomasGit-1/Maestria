# import cv2
# import numpy as np
# from skimage import measure
# from skimage.measure import regionprops


# # Cargar la imagen
# image_path = 'all-tools-small.tif'
# src = cv2.imread(image_path)

# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# I = abs(255-gray)
# #obtaing contours 
# contours, _ = cv2.findContours(I, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(src, contours, -1, (0,255,0), 2, cv2.LINE_AA)
# # Mostrar la imagen
# cv2.imshow('Contours', src)
# cv2.waitKey(0)
# cv2.destroyAllWindows()