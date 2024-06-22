import numpy as np
from ANN import ANN

# Ejemplo de entrenamiento y uso de la red neuronal
if __name__ == "__main__":
    X = np.array([[0, 0],
                  [0, 1],
                  [1, 0],
                  [1, 1]])    
    y = np.array([[0],
                  [1],
                  [1],
                  [0]])
    
    # Crear la red neuronal
    ann = ANN(inputLayer=2,
                hiddenLayers=2,
                outputLayer=1,
                learningRate=0.1,
                X_true = X,
                Y_true = y)
    
    # Entrenar la red neuronal
    ann.train()
    
    # # Uso de la red neuronal
    # print(ann.predict(np.array([0, 0])))
    # print(ann.predict(np.array([0, 1])))
    # print(ann.predict(np.array([1, 0])))
    # print(ann.predict(np.array([1, 1])))