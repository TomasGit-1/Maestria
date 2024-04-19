import math
import numpy as np
from scipy.spatial.distance import cdist
import random
import matplotlib.pyplot as plt

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
    return random.random() < math.exp(- deltaE / T)

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

def simulated_annealing(Tmax, Tmin, Eth, alpha, citys,distance):
    T = Tmax
    X =generate_solution(citys)
    E = compute_energy(X,distance)
    T_values = []
    E_values = []

    while T > Tmin and E > Eth:
        Xnew = generate_solution(X)
        Enew = compute_energy(Xnew,distance)
        deltaE = Enew - E
        if accept(deltaE, T):
            X = Xnew
            E = Enew
        T = T / alpha
        T_values.append(T)
        E_values.append(E)

    solucion = [(index, citys[index]) for index in X]
    return solucion


if __name__ == '__main__':
    filename = "kroA100/kro100.tsp"
    citys = read_file(filename)
    distance = calculate_distance(citys)

    Tmax = 20
    Tmin = 10
    alpha = 1.9
    Eth = 100
    solution = simulated_annealing(Tmax, Tmin, Eth, alpha,citys,distance)
    plot_cities(citys,distance)
    plots_solution(solution,distance)

    print(solution)

