from PGenetica import PGenetica
from binarytree import Node,build
from sklearn.datasets import make_regression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size  = comm.Get_size()



# Generar datos de entrada (X)
np.random.seed(42)
X = np.linspace(1, 2 * np.pi, 100)
# Añadir ruido a los datos3
y = np.sin(X) + np.random.normal(0, 0.1, X.shape)

objGenetica = PGenetica(X,y,limite=200)

print("Primera geneacion")
if rank == 0:
    poblacion = objGenetica.generatePoblacionAleatoria(poblacionSize=100,profundidad=4)
else:
    poblacion = None

print("Dividir la población entre los nodos")
# Dividir la población entre los nodos
if rank == 0:
    sub_poblaciones = np.array_split(poblacion, size)
else:
    sub_poblaciones = None

sub_poblacion = comm.scatter(sub_poblaciones, root=0)

for i in range(10):
    antiguaGeneracion = sub_poblacion
    nuevaGeneracion =objGenetica.generateGeneration(antiguaGeneracion)
    
    NuevaG = comm.gather(nuevaGeneracion, root=0)
    if rank == 0:
        """
            Tomamso los mejores 50% de la Antigua Generacion y los 50% mejores de la nmueva generaion
        """
        sub_poblacion = antiguaGeneracion[len(antiguaGeneracion)//2:] + NuevaG[len(NuevaG)//2:]
    sub_poblacion = comm.bcast(sub_poblacion, root=0)

poblacion_completa = comm.gather(sub_poblacion, root=0)
if rank == 0:    
    print(poblacion_completa)
    # poblacion_completa = [ind for sublist in poblacion_completa for ind in sublist]
    df = pd.DataFrame(poblacion_completa)
    numero_entero = random.randint(1, 100)  # Genera un número entero aleatorio entre 1 y 100 (ambos inclusive)
    df.to_csv(f"poblacionCompleta{str(numero_entero)}.csv")
