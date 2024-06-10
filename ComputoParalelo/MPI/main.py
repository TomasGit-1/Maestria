from PGenetica import PGenetica
from binarytree import Node,build
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import numpy as np

# Generar datos de entrada (X)
np.random.seed(42)
X = np.linspace(1, 2 * np.pi, 100)
# Añadir ruido a los datos3
y = np.sin(X) + np.random.normal(0, 0.1, X.shape)

objGenetica = PGenetica(X,y)
poblacion = objGenetica.generatePoblacionAleatoria(poblacionSize=4)
print("Primera geneacion")
# for i in range(len(poblacion)):
#     print(poblacion[i]["tree"])
# print(30*"#")

for i in range(100):
    poblacion =objGenetica.generateGeneration(poblacion)

# print("Ultima geneacion")
# for i in range(len(poblacion)):
#     print(poblacion[i]["tree"])
print(30*"#")



# # Graficar los datos
# plt.scatter(X, y, color='blue', label='Datos')
# plt.plot(X, np.sin(X), color='red', label='Función original (sin(x))')
# plt.xlabel('X')
# plt.ylabel('y')
# plt.title('Datos generados')
# plt.legend()
# plt.show()