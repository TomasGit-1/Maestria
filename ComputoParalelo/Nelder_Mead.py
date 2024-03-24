# from random import random
import random
import math
import numpy as np
import matplotlib.pyplot as plt
def sphere(x):
    return sum(item**2 for item in x)

def createPop(dim,puntos):
    try:
        li, ls = -10, 10
        S = []
        for _ in range(puntos):
            p1 = [0]
            #Coordenadas
            # [ li + random() * (ls - li) for _ in range(dim)]
            p1.extend([ random.randint(li, ls) for _ in range(dim)])
            #contiene el valor de la función de esfera
            p1[0] = sphere(p1[1:])
            S.append(p1)
        return S
    except Exception as e:
        raise Exception(f'Error en createPop : {str(e)}')
    
def sortPop(S):
    try:
        S.sort(key=lambda x: x[0])
        return S
    except Exception as e:
        raise Exception(f'Error en sortPop : {str(e)}')
    
def determineMass(S):
    try:
        #Solo se ocupan las coordenadas
        mass = [sum(col) / len(S) for i, col in enumerate(zip(*S)) if i > 0]
        # mass = [ sum(col)/len(S) for col in  list(zip(*S))]
        return mass
    except Exception as e:
        print(str(e))

def reflection(m, reflection, peor):
    try:
        ref = [ item[0] + (reflection * (item[0] - item [1] )) for item in  zip(m , peor)]
        return ref
    except Exception as e:
        raise Exception(f"Error en reflection {str(e)}")

def expansion(r, expansion, m ):
    try:
        exp = [ item[0] + (expansion * (item[0] - item [1] )) for item in  zip(r , m)]
        return exp
    except Exception as e:
        raise Exception(f"Error en expansion {str(e)}")

def contraction(r , Contraction , m  ):
    try:
        contraT = [ (Contraction * rItem) + ((1 - Contraction) * mItem) for rItem, mItem in zip(r,m)]
        return contraT
    except Exception as e:
        raise Exception(f"Error en contraction {str(e)}")


def Shrink(S, shrink):
    try:
        # contraT = [ (Contraction * rItem) + ((1 - Contraction) * mItem) for rItem, mItem in zip(r,m)]
        # return contraT
        best_solution = S[0]
        for i in range(len(S)-1, 0, -1 ):
            Z = [0]
            Z.extend([best_solution[j] + shrink * (S[i][j] - best_solution[j]) for j in range(len(S[i])) if j > 0])
            Z[0] = sphere(Z[1:])
            S[i] = Z
        return S
    except Exception as e:
        raise Exception(f"Error en contraction {str(e)}")

def euclidean_distance(point1, point2):
    """Calcula la distancia euclidiana entre dos puntos."""
    squared_sum = sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2))
    return math.sqrt(squared_sum)

def check_simplex_distance(S, tol):
    """Verifica si la distancia entre los puntos del simplex es menor que la tolerancia."""
    return True if euclidean_distance(S[0],S[-1]) > tol  else False

def objective_function(x, y):
    return -(x**2 + y**2)


def graficar(simplex):
    # Rango de valores para x e y
    x_values = np.linspace(0, 150, 100)
    y_values = np.linspace(-10, 40, 100)
    # Crear una malla de valores para x e y
    X, Y = np.meshgrid(x_values, y_values)
    # Función objetivo (ejemplo)
    Z_obj = objective_function(X, Y)
    # Crear el contorno de la función objetivo
    plt.contour(X, Y, Z_obj, levels=20, cmap='viridis') 
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
    return plt


def main():
    try:
        space_optimizations = []
        n = 2
        Reflection = 1
        Expansion =2
        Contraction = 0.5
        shrink = 0.5
        #Creando el Simplex 
        S = createPop(n, n+1)
        print("\n".join(str(s) for s in S))
        print("#" * 100)
        tolerancia = 0.01
        spinning = 0
        # while spinning < 100:
        while check_simplex_distance(S, tolerancia):
            #Ordenamos
            S = sortPop(S)
            space_optimizations.extend([np.array(S)])

            #print("\n".join(str(s) for s in S))
            #Calculamos el centro de masa quitamos el pero punto
            M = determineMass(S[:n])
            #print("\n".join(str(m) for m in M))
            #Reflection: reflect the worst point over m
            R = reflection(M, Reflection, S[n][1:])
            fR = sphere(R)
            #Ocupo por indices por que ya esta calculado el funcion del esfera
            #if sphere(S[0]) < sphere(R) < sphere(S[-1]):
            if S[0][0] < fR < S[n][0]:
                R.insert(0,fR)
                S[n] = R
            else:
                if fR <= S[0][0]:
                    #Expansion: try to search farther in this direction
                    E = expansion(R , Expansion , M )
                    fE = sphere(E) 
                    if fE < fR:
                        E.insert(0,fE)
                        S[n] = E #Deep COpy , Copy
                    else:
                        R.insert(0,fR)
                        S[n] = R
                else:
                    b = True
                    # -2 = n-1
                    if fR >= S[n-1][0]:
                        #Contraction: a test point between r and m
                        C = contraction(R, Contraction , M)
                        fC = sphere(C)
                        if fC < fR:
                            C.insert(0,fC)
                            S[n] = C
                            b = False
                    if b == True:
                        #Shrink towards the best solution candidate S[0]
                        S = Shrink(S, shrink)
            spinning +=1
        print("\n".join(str(s) for s in S))
        return space_optimizations
    except Exception as e:
        print(f"Error en main : {str(e)}")

    
simplex = main()
# plt = graficar(S) 
    # Rango de valores para x e y
x_values = np.linspace(0, 150, 100)
y_values = np.linspace(-10, 40, 100)
# Crear una malla de valores para x e y
X, Y = np.meshgrid(x_values, y_values)
# Función objetivo (ejemplo)
Z_obj = objective_function(X, Y)
# Crear el contorno de la función objetivo
plt.contour(X, Y, Z_obj, levels=20, cmap='viridis') 
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']  # Puedes agregar más colores si es necesario
# Graficar cada triángulo del simplex (ejemplo)
for idx, s in enumerate(simplex):
    # Extraer las coordenadas x, y, z de los puntos del triángulo
    x = s[:, 0]
    y = s[:, 1]
    z = s[:, 2]
    # color = plt.cm.rainbow(idx / len(simplex))  # Utilizamos un mapa de colores
    color = colors[idx % len(colors)]  # Ciclo de colores si hay más triángulos que colores
    # Conectar los puntos del triángulo
    for i in range(len(s)):
        plt.plot([x[i], x[(i+1)%len(s)]], [y[i], y[(i+1)%len(s)]], 'b--',color=color)

# Etiquetas de los ejes y título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contouring the Solution Space of Optimization')

# Mostrar el gráfico
plt.grid(True)
plt.show()
