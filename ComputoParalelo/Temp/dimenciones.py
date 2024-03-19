import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Función para generar puntos aleatorios en el espacio de n dimensiones
def generar_puntos(n, num_puntos):
    puntos = np.random.rand(num_puntos, n)
    return puntos

# Función para visualizar el simplex en 2D
def visualizar_simplex_2d(puntos):
    plt.scatter(puntos[:, 0], puntos[:, 1])
    plt.plot(puntos[:, 0], puntos[:, 1], 'r-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Simplex en 2D')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Función para visualizar el simplex en 3D
def visualizar_simplex_3d(puntos):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(puntos[:, 0], puntos[:, 1], puntos[:, 2])
    ax.plot_trisurf(puntos[:, 0], puntos[:, 1], puntos[:, 2], linewidth=0.2, antialiased=True)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Simplex en 3D')
    plt.show()

# Generar puntos en diferentes dimensiones
dimensiones = 3  # Cambiar a 3 para visualizar en 3D
num_puntos = dimensiones + 1
puntos = generar_puntos(dimensiones, num_puntos)

# Visualizar el simplex
if dimensiones == 2:
    visualizar_simplex_2d(puntos)
elif dimensiones == 3:
    visualizar_simplex_3d(puntos)
else:
    print("La visualización en {} dimensiones no está implementada.".format(dimensiones))
