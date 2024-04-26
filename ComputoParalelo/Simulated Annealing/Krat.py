import math
import numpy as np
from scipy.spatial.distance import cdist
import random
import matplotlib.pyplot as plt
import time
def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        tspStart = lines.index('NODE_COORD_SECTION\n') + 1
        tspFinish= lines.index('EOF\n')
        # cityList = [tuple(map(float, l.strip().split()[1:])) for l in lines[tspStart:tspFinish]]
        cityArray = np.loadtxt(lines[tspStart:tspFinish], usecols=(1, 2))
        return cityArray

def find_distance(city1, city2):
    return math.sqrt((city1[1] - city2[1])**2 + (city1[2] - city2[2])**2)

def calculate_distance(citys):
    distancias = cdist(citys, citys, 'euclidean')
    return np.array(distancias)

def generate_solution(citys):
    return np.random.permutation(len(citys))

def compute_energy(X,distance):
    total_distance = 0
    n = len(X)
    for i in range(n-1):
        city1 = X[i]
        dcity2 = X[i + 1]
        total_distance += distance[city1][dcity2]
    total_distance += distance[X[-1]][X[0]]  # Agregar la distancia de regreso a la primera ciudad
    return total_distance

def accept(deltaE, T):
    if deltaE < 0:
        return True
    result = random.random() < math.exp(- deltaE / T)
    return result

def plot_cities(cities , distance_matrix=None):
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', zorder=1)
    
    for i, city in enumerate(cities):
        plt.text(city[0], city[1], str(i), fontsize=12, ha='center', va='center')

    n = len(cities)
    for i in range(n):
        for j in range(i+1, n):
            distance = distance_matrix[i][j]
            plt.plot([cities[i][0], cities[j][0]], [cities[i][1], cities[j][1]], color='gray', linestyle='--', linewidth=0.5)
            plt.text((cities[i][0] + cities[j][0]) / 2, (cities[i][1] + cities[j][1]) / 2, f'{distance:.2f}', fontsize=8, color='black')
    plt.title('Cities')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def plot_values(T_values, E_values):
    plt.plot(T_values, label='Temperature')
    plt.plot(E_values, label='Energy')
    plt.xlabel('Iterations')
    plt.ylabel('Value')
    plt.legend()
    plt.pause(0.01)  

def plots_solution(solucion,distance_matrix=None):
    # Extraer las coordenadas X e Y de las ciudades
    x = [city[1][0] for city in solucion]
    y = [city[1][1] for city in solucion]

    # Graficar las ciudades como puntos
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, color='blue', zorder=1)
    
    # Etiquetar las ciudades con su índice
    for index, coordinates in solucion:
        plt.text(coordinates[0], coordinates[1], str(index), fontsize=12, ha='center', va='center')
    
    for i in range(len(solution) - 1):
        city1 = solution[i]
        city2 = solution[i + 1]
        distance = distance_matrix[city1[0]][city2[0]]
        coordinates1 = city1[1]
        coordinates2 = city2[1]
        plt.plot([coordinates1[0], coordinates2[0]], [coordinates1[1], coordinates2[1]], color='gray', linestyle='--', linewidth=0.5)
        plt.text((coordinates1[0] + coordinates2[0]) / 2, (coordinates1[1] + coordinates2[1]) / 2, f'{distance:.2f}', fontsize=8, color='black')
    
    city1 = solution[-1]
    city2 = solution[0]
    distance = distance_matrix[city1[0]][city2[0]]
    coordinates1 = city1[1]
    coordinates2 = city2[1]
    plt.plot([coordinates1[0], coordinates2[0]], [coordinates1[1], coordinates2[1]], color='gray', linestyle='--', linewidth=0.5)
    plt.text((coordinates1[0] + coordinates2[0]) / 2, (coordinates1[1] + coordinates2[1]) / 2, f'{distance:.2f}', fontsize=8, color='black')


    plt.title('Cities')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


def generate_solution2OTP(X_new,distance):
    improved = True
    while improved:
        improved = False
        for i in range(len(X_new) - 1):
            for j in range(i + 2, len(X_new)):
                if j - i == 1:
                    continue
                new_solution = np.concatenate((X_new[:i], X_new[i:j][::-1], X_new[j:]))
                new_distance = compute_energy(new_solution, distance)
                if new_distance < compute_energy(X_new, distance):
                    X_new = new_solution
                    improved = True
                    break
            if improved:
               break
    return X_new
    
def Generate_2opt(X_new, distance):
    minChange = 0
    for i in range(len(X_new) - 2):
        for j in range(i + 2 , len(X_new) - 1):
            costA =  distance[X_new[i]][X_new[i+1]]  +  distance[X_new[j]][X_new[j+1]]
            costN =  distance[X_new[i]][X_new[j]]  +  distance[X_new[i]][X_new[j+1]]
            change = costN - costA
            if change < minChange:
                minChange = change
                min_i = i
                min_j = j
    if minChange < 0:
        X_new[min_i+1:min_j+1] = X_new[min_i+1:min_j+1][::-1]
    
    return X_new


def generate_solution2OPT1(X_new,previous_solutions):
    while True:
        i, j = random.sample(range(len(X_new)), 2) 
        i, j = min(i, j), max(i, j)
        new_solution = np.copy(X_new)
        new_solution = np.copy(X_new)
        if len(X_new[j-1:i-1:-1]) == 0:
            return X_new , previous_solutions
        
        new_solution[i:j] = X_new[j-1:i-1:-1]
        if tuple(new_solution) not in previous_solutions:
            previous_solutions.add(tuple(new_solution))
            return new_solution,previous_solutions

    
def simulated_annealing(Tmax, Tmin, Eth, alpha, citys,distance):
    T = Tmax
    X =generate_solution(citys)
    E = compute_energy(X,distance)
    print(f"Ajuste de energia {str(T)}  E {str(E)}")

    step = 1
    while (T > Tmin) and (E > Eth):
        Xnew = generate_solution2OTP(X,distance)
        Enew = compute_energy(Xnew,distance)
        deltaE = Enew - E
        if accept(deltaE, T):
            X = Xnew
            E = Enew
        #https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/
        # T = T / (step * alpha)
        T = alpha * T 
        # T =  T / alpha 


        print(f"Ajuste de energia {str(T)}  E {str(E)}")
        step+=1
        if math.isinf(T):
            print("La temperatura ha alcanzado 'inf'. El algoritmo ha convergido o ha llegado a su límite de iteración.")
            print(f"Error Minimo {E}")
            break

    solucion = [(index, citys[index]) for index in X]
    return solucion


# def simulated_annealingV2(Tmax, Tmin, Eth, alpha, citys,distance):
#     T = Tmax
#     X =generate_solution(citys)
#     E = compute_energy(X,distance)
#     previous_solutions = [X]  # Lista para almacenar las soluciones anteriores
#     previous_solutions = set()
#     previous_solutions.add(tuple(X))
#     print(f"Ajuste de energia {str(T)}  E {str(E)}")

#     step = 1
#     while (T > Tmin) and (E > Eth):
#         Xnew,previous_solutions = generate_solution2OPT1(X,previous_solutions) 
#         Enew = compute_energy(Xnew,distance)
#         deltaE = Enew - E
#         if accept(deltaE, T):
#             X = Xnew
#             E = Enew
#         #https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/
#         # T = T / (step * alpha)
#         T = alpha * T 
#         T =  T / alpha 

#         print(f"Ajuste de energia {str(T)}  E {str(E)}")
#         step+=1
#         if math.isinf(T):
#             print("La temperatura ha alcanzado 'inf'. El algoritmo ha convergido o ha llegado a su límite de iteración.")
#             print(f"Error Minimo {E}")
#             break

#     solucion = [(index, citys[index]) for index in X]
#     return solucion


if __name__ == '__main__':
    start_time = time.time()
    filename = "kroA100.tsp"
    citys = read_file(filename)
    distance = calculate_distance(citys)
    Tmax = 1000
    Tmin = 10
    alpha = 0.8
    Eth = 21282
    solution = simulated_annealing(Tmax, Tmin, Eth, alpha,citys,distance)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Tiempo transcurrido:", elapsed_time, "segundos")
    plot_cities(citys,distance)
    plots_solution(solution,distance)
    print(solution)

