import numpy as np 
import matplotlib.pyplot as plt
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
#https://aws.amazon.com/es/what-is/logistic-regression/

class LogisticRegression():

    def __init__(self):
        pass

    def get_data(self, weight, sesgo):
        self.weight = weight
        self.sesgo = sesgo

    def generate_grafica(self, X_train, X_test, y_train, y_test):
        plt.figure(figsize=(8, 6))
        plt.scatter(X_train[:, 0], X_train[:, 1], c='b', marker='o', label='Conjunto de Entrenamiento')
        plt.scatter(X_test[:, 0], X_test[:, 1], c='r', marker='x', label='Conjunto de Prueba')
        plt.xlabel('Característica 1')
        plt.ylabel('Característica 2')
        plt.title('Conjuntos de Entrenamiento y Prueba')
        plt.legend()
        plt.show()

    def generate_Train(self):
        # Generar datos aleatorios
        np.random.seed(0)
        # Creamos 100 muestras con 2 características
        X = np.random.randn(100, 1)
        # Asignamos etiquetas 0 o 1 a cada muestra
        y = np.random.randint(0, 2, size=100)
        # Dividir los datos en conjuntos de entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    

    def generate_GZ(self, Z):
        gz = 1 / (1 + np.exp(-Z))

        # plt.figure(figsize=(8, 6))
        # plt.plot(gz, marker='o', linestyle='-')
        # plt.xlabel('Índice')
        # plt.ylabel('g(z)')
        # plt.title('Gráfico de la salida de la función sigmoide')
        # plt.axhline(y=0.5, color='gray', linestyle='--', linewidth=0.8)  # Línea horizontal en y=0.5 para indicar el punto medio
        # plt.grid(True, linestyle='--', alpha=0.7)
        # plt.show()
        return gz
    
    def derivada_parcial_b_w(self, Y, X):
        d_w = 0
        d_b = 0
        f_wb = np.dot(X ,self.weight) + self.sesgo - Y
        d_w = np.dot(f_wb, X)
        d_b = np.sum(f_wb)

        return d_w / Y.shape[0], d_b / Y.shape[0]
    
    def generate_gradiente(self,alpha , d_w , d_b):
        w = self.weight - alpha * d_w
        b = self.sesgo - alpha * d_b
        return w, b

    def compute_model_output(self,X):
        return np.dot(X, self.weight) + self.sesgo

if __name__ == "__main__":
    #Instance of the Model class
    RL = LogisticRegression()
    #Generate the training and test data for the model
    X_train, X_test, y_train, y_test = RL.generate_Train()
    #Optional, Generate the graphical representation of the data, 
    #RL.generate_grafica(X_train, X_test, y_train, y_test)
    #Inictialize the parameters of the model
    n_samples, n_cha = X_train.shape
    w = np.zeros(n_cha)
    b = 0
    RL.get_data(w, b)
    alpha = 0.001
    i = 0
    
    while True:
        print(f" Learning rate {i} ,  loss = {1}, w = {RL.weight }, b = {RL.sesgo}")
        Z = RL.compute_model_output(X_train)
        d_w ,d_b = RL.derivada_parcial_b_w(y_train, X_train)
        w_temp,b_temp =RL.generate_gradiente(alpha , d_w , d_b)
        gz = RL.generate_GZ(Z)
        if w_temp - RL.weight <= 0.000001:
            break
        RL.get_data(w_temp, b_temp)
        y_predict = RL.compute_model_output(X_train)
        i += 1
        