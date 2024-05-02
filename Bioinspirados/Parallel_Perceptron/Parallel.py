from sklearn.model_selection import train_test_split
from sklearn.datasets import make_moons
from sklearn.preprocessing import MinMaxScaler
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score

def generate_Train():
    X,y = make_moons(n_samples=600, noise=0.20)

    #división del conjunto de datos 
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y)

    #escalamiento del conjunto de datos
    escalador = MinMaxScaler()
    X_tr = escalador.fit_transform(X_tr)
    X_te = escalador.transform(X_te)

    #union de conjuntos de datos escalados entrenamiento y prueba (para graficar)
    X_t = np.vstack((X_tr,X_te))
    y_t = np.vstack((y_tr.reshape(-1,1),y_te.reshape(-1,1)))

    #grafica del conjunto de datos escalados y dividos
    plt.scatter(X_tr[:,0], X_tr[:,1], c = y_tr)
    plt.scatter(X_te[y_te == 0,0], X_te[y_te == 0,1], marker='x', c = 'red')
    plt.scatter(X_te[y_te == 1,0], X_te[y_te == 1,1], marker='+', c = 'green')
    # plt.show()
    return X_tr, X_te, y_tr, y_te,X_t,y_t

class PerceptronParalelo():
    def __init__(self, epochs=100, n=3, error=0.1):
        self.epochs =epochs
        self.n= n
        self.error=error

    def fit(self, X,y):
        rows = X.shape[0]
        dim = X.shape[1] + 1            
        ext = np.ones((rows, 1))
        eXtr = np.hstack((X, ext))
        eXtr = [x / np.linalg.norm(x) for x in eXtr]
        #Normalizar todos los datos divirdos sobre su norma
        e=0.01
        m=1
        yi=0.05
        self.vectorWeight =[np.copy(np.random.uniform(low=0,high=1, size=dim)) for _ in range(self.n)]
        self.vectorWeight = [w / np.linalg.norm(w) for w in self.vectorWeight]
        #Normalizar todos los datos divirdos sobre su norma

        for _ in range(self.epochs):
            suma_predicciones=0
            predict = self.predict(X)
            suma_predicciones = sum(predict)
            sp= self.squaching(suma_predicciones)

            for i in range(len(self.vectorWeight)):
                alpha= self.vectorWeight[i]

                if np.all(np.abs(sp - y) <= e):
                    #The parallel perceptron is correct up to this accuracy 
                    pass
                if np.all( sp > y + e ):
                    delta = -eXtr
                    
                if np.all( sp > y +self.error) and predict[i] >= 0:
                    delta=-eXtr
                elif np.all(sp < y -self.error) and predict[i] < 0:
                    delta=eXtr
                else:
                    delta = np.zeros(dim)       

                alpha += self.error  * delta
                self.vectorWeight[i] = alpha

    def predict(self, X):
        rows = X.shape[0]
        ext = np.ones((rows, 1))
        eX = np.hstack((X, ext))
        y_hat = np.zeros(rows)
        predic = []
        for w in range(len(self.vectorWeight)):
            for i, x in enumerate(eX):
                y_hat[i] = 1 if np.dot(x, self.vectorWeight[w]) >= 0 else -1
            predic.append(y_hat)
        return predic
        
    def score(self,X,y):
        return accuracy_score(y, self.predict(X))
    
    def squaching(self, p):
        result = np.where(p<0,-1,p)
        result= np.where(p>=0,1,result)
        return result
    
def graficar_frontera_decision(modelo, X, y):
    feature_1, feature_2 = np.meshgrid(
        np.linspace(np.min(X[:,0]), np.max(X[:,0])),
        np.linspace(np.min(X[:,1]), np.max(X[:,1])))

    grid = np.vstack([feature_1.ravel(), feature_2.ravel()]).T

    pred = modelo.predict(grid)
    pred = np.reshape(pred, feature_1.shape)
    display = DecisionBoundaryDisplay(
        xx0=feature_1, xx1=feature_2, response=pred)
    display.plot()
    display.ax_.scatter(
        X[:, 0], X[:, 1], c=y, edgecolor="black"
    )
    plt.show()
    
if __name__ == "__main__":
    
    X_tr, X_te, y_tr, y_te,X_t,y_t = generate_Train()
    ppa = PerceptronParalelo(epochs=100, n=3, error=0.1)
    ppa.fit(X_tr, y_tr)
    graficar_frontera_decision(ppa, X_t, y_t)