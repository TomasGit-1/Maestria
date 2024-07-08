import cv2
import numpy as np

# Cargar la imagen
image_path = 'all-tools-small.tif'
src = cv2.imread(image_path)

# Convertir a escala de grises
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# Invertir la imagen
I = abs(255 - gray)

# Obtener contornos
contours, _ = cv2.findContours(I, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos sobre la imagen original
cv2.drawContours(src, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)
label_counter = 0

# Calcular y mostrar las propiedades de los contornos
for contour in contours:
    # Calcular el área
    area = cv2.contourArea(contour)
    
    # Calcular el perímetro
    perimeter = cv2.arcLength(contour, True)
    
    # Calcular el bounding box
    x, y, w, h = cv2.boundingRect(contour)
    cv2.putText(src, f"{label_counter} area: {round(area,2)} _ Perimetro: {round(perimeter,2)}", (x, y - 2), cv2.FONT_HERSHEY_PLAIN, 0.8, (255, 0, 255), 1)

    cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Calcular el centroide
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0
    cv2.circle(src, (cx, cy), 5, (255, 0, 0), -1)
    # cv2.putText(src, f"Centroide: ({cx}, {cy})", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)

    label_counter += 1



# Mostrar la imagen con las propiedades calculadas
cv2.imshow('Contours with Properties', src)
cv2.waitKey(0)
cv2.destroyAllWindows()



    
    # # Mostrar las propiedades de cada contorno
    # print(f"Área: {area}")
    # print(f"Perímetro: {perimeter}")
    # print(f"Bounding box: (x={x}, y={y}, w={w}, h={h})")
    # print(f"Centroide: (x={cx}, y={cy})")
    # print()