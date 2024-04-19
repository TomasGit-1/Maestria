'''
TODO
Implementar clasificador descrito en (Auer2008) A Learning Rule for Very Simple Universal Approximators Consisting of a Single Layer of Perceptrons
Se sugiere seguir la estructura de método fit para entrenar y predict para realizar inferencias para poder usar los métodos y funciones ya establecidos
Los hiperparametros del modelo deben poder ser definidos en el constructor del modelo
'''

from sklearn.datasets import make_moons
from sklearn.preprocessing import MinMaxScaler
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Perceptron_Paralelo:
    def __init__(self ,epochs = 1000, n=10) -> None:
        self.w = None
        self.epochs = epochs
        self.n = n
    
    def fit(self, X, y):
        #Vector normarlizado para los pesos 
        #Cuantos Perceptrones vamos a tener
        #Alpha Para el perceptron [1, -1]
        #Se suman las salidas del perceptron
        #p > 0 == 1  p < 0 -1
        rows  = X.shape[0]
        dim = X.shape[1] + 1
        ext = np.ones((rows, 1))
        eXtr = np.hstack((X, ext))
        p = 0 
        self.weights = np.copy(np.random.uniform(low = 0, high = 1, size = dim))     

        for _ in range(self.epochs):
            #Numero de perceptron
            for xi in range(rows):
                for _ in range(self.n):
                    wTemp = np.copy(np.random.uniform(low = 0, high = 1, size = rows))     
                    p += self.predict(X,wTemp)
                sp = self.squashing(p)
            
            
    def squashing(self, p):
        return 1 if p>= 0 else -1
    
    def squashing_rho(self, p , rho):
        if p <= -rho:
            return -1
        elif -rho < p < rho:
            return p / rho
        else:
            return 1


    #método para calcular la exactitud
    def score(self, X, y):
        return accuracy_score(y, self.predict(X))
    
    #método para hacer inferencias
    def predict(self, X, wTemp):
        deltaaz = 0
        for zi, deltai in zip(X, wTemp):
            deltaaz += zi * deltai
        return 1 if deltaaz >= 0 else -1
    


if __name__ == '__main__':
    #división del conjunto de datos
    X,y = make_moons(n_samples=600, noise=0.20) 
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y)

    #escalamiento del conjunto de datos
    escalador = MinMaxScaler()
    X_tr = escalador.fit_transform(X_tr)
    X_te = escalador.transform(X_te)

    ppa = Perceptron_Paralelo()
    ppa.fit(X_tr, y_tr)

    print(f'[Percpetron Paralelo] Exactitud en Entrenamiento {ppa.score(X_tr, y_tr)}')
    print(f'[Percpetron Paralelo] Exactitud en Prueba {ppa.score(X_te, y_te)}')
        