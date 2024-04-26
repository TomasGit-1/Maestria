from time import time
import numpy as np
from numba import njit

def evaluate_sphere(x):
    return np.sum(x**2, axis=1 )

@njit
def evaluate_sphere_numba(x):
    return np.sum(x**2, axis=1)

if __name__ == '__main__':
    li, ls = -10, 10
    pop_n, dim_n = 100, 10
    pop = np.random.uniform(li, ls, size = (pop_n, dim_n))
    runs = 22
    tiempos = np.zeros(runs)
    for i in range(runs):
        start = time()
        pop = np.random.uniform(li, ls, size = (pop_n, dim_n))
        evaluate_sphere(pop)
        tiempos[i] = time() - start

    tiempos_numba = np.zeros(runs)
    for i in range(runs):
        start = time()
        pop = np.random.uniform(li, ls, size = (pop_n, dim_n))
        evaluate_sphere_numba(pop)
        tiempos_numba[i] = time() - start
        

    print(np.mean(tiempos), np.std(tiempos))
    print(np.mean(tiempos_numba), np.std(tiempos_numba))
    

                            