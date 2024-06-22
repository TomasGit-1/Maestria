#Librerias externas
import matplotlib.pyplot as plt
import numpy as np

#Modulos
from ANN import ANN
from utils import generateSample, paintXYPlot

# Ejemplo de entrenamiento y uso de la red neuronal
if __name__ == "__main__":
    n_features = 5
    n_classes = 2
    X, y = generateSample(n_features=n_features, n_classes=n_classes)

    ann = ANN(X_true = X,Y_true = y)
    ann.train()
    