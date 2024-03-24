import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



# Definición de los puntos de los triángulos
simplex = [
    np.array([[13, -2, 3], [90, -3, 9], [130, 9, 7]]),
    np.array([[10, 10, 8], [20, 25, 22], [30, 35, 32]]),
    np.array([[0, 0, 0], [5, 0, 0], [0, 5, 0]]),
    # Añade más puntos de triángulos si lo deseas
]

# Crear una figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar cada triángulo
for s in simplex:
    x = s[:, 0]
    y = s[:, 1]
    z = s[:, 2]
    for i in range(len(s)):
        ax.plot([x[i], x[(i+1)%len(s)]], [y[i], y[(i+1)%len(s)]], [z[i], z[(i+1)%len(s)]], 'b--')

# Etiquetas de los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Mostrar el gráfico
plt.show()


