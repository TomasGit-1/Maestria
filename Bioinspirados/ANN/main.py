#Librerias externas
from sklearn.model_selection import train_test_split
from colorlog import ColoredFormatter
import matplotlib.pyplot as plt
import numpy as np
import logging
#Modulos
from ANN import ANN
from utils import generateSample, paintXYPlot, downloadDatasets

logger = logging.getLogger()
logger.setLevel(logging.INFO) 

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# Ejemplo de entrenamiento y uso de la red neuronal
if __name__ == "__main__":
    # n_features = 5
    # n_classes = 2
    # X, y = generateSample(n_features=n_features, n_classes=n_classes)
    nameDataset = "balance"
    X, y = downloadDatasets(logger, nameDataset)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ann = ANN(log = logger,nameDataset = nameDataset, X_true = X_train, Y_true = y_train, neuronal = 5)
    ann.train()
    