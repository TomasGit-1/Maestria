#NearMead
import numpy as np

def sphere(x):
    return np.sum(x**2, axis=1)

funcion = sphere

li, ls = -10, 10
dim = 2
#Poblacion
pop_size = 10
iteraciones = 10
pop_sel = 4
pop = np.random.uniform(li, ls, size=(pop_size, dim))
fitness = funcion(pop)
fitness_sort = np.argsort(fitness)
print(fitness[fitness_sort[0]], pop[fitness_sort[0]])

for i in range(iteraciones):
    
    pop_median = np.mean(pop[fitness_sort[:pop_sel]], axis=0)
    pop_std = np.std(pop[fitness_sort[:pop_sel]], axis=0)

    pop = np.random.normal(pop_median, pop_std, size=(pop_size, dim))
    fitness = funcion(pop)
    fitness_sort = np.argsort(fitness)
    
    print(pop_median, pop_std)

