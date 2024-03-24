import numpy as np
import matplotlib.pyplot as plt

# Definición de los puntos del simplex
simplex = [
    np.array([[13, -2, 3], [90, -3, 9], [130, 9, 7]]),
    np.array([[10, 10, 8], [20, 25, 22], [30, 35, 32]]),
    np.array([[0, 0, 0], [5, 0, 0], [0, 5, 0]]),
    # Añade más puntos de triángulos si lo deseas
]
def objective_function(x, y):
    return -(x**2 + y**2)

# Rango de valores para x e y
x_values = np.linspace(0, 150, 100)
y_values = np.linspace(-10, 40, 100)

# Crear una malla de valores para x e y
X, Y = np.meshgrid(x_values, y_values)

# Función objetivo (ejemplo)
Z_obj = objective_function(X, Y)

# Crear el contorno de la función objetivo
plt.contour(X, Y, Z_obj, levels=20, cmap='viridis')  # Contornos de la función objetivo

# Graficar cada triángulo del simplex (ejemplo)
for s in simplex:
    # Extraer las coordenadas x, y, z de los puntos del triángulo
    x = s[:, 0]
    y = s[:, 1]
    z = s[:, 2]
    # Conectar los puntos del triángulo
    for i in range(len(s)):
        plt.plot([x[i], x[(i+1)%len(s)]], [y[i], y[(i+1)%len(s)]], 'b--')

# Etiquetas de los ejes y título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contouring the Solution Space of Optimization')

# Mostrar el gráfico
plt.grid(True)
plt.show()
