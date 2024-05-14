from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def sphere(x):
    return np.sum(x**2, axis=1)

funcion = sphere
li, ls = -10, 10
dim = 2
pop_size = 10
iteraciones = 10
pop_sel = 5

try:
    pop_size = (int(sys.argv[1])//size)
except:
    pass

node_pop = np.random.uniform(li, ls, size=(pop_size, dim))
node_fitness = funcion(node_pop)
