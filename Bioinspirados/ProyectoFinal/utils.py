from colorlog import ColoredFormatter
from ucimlrepo import fetch_ucirepo 
import pandas as pd
import logging
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import uuid
import os
import seaborn as sns
from sklearn.metrics import confusion_matrix,accuracy_score

def plot_confusion_matrix(Y_true, y_pred,exactitud):
    conf_matrix = confusion_matrix(Y_true, y_pred)
    classes = np.unique(Y_true)

    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='g', cbar=False,
                xticklabels=classes, yticklabels=classes)
    plt.xlabel('Etiquetas Predichas')
    plt.ylabel('Etiquetas Verdaderas')
    plt.title('Matriz de Confusión\nExactitud: {:.2f}'.format(exactitud))
    random_filename = str(uuid.uuid4())
    plt.savefig(f"figures/Matriz_predicciones_{random_filename}.png")
    plt.show()

    # Fila 1: Representa la clase 0.
    # 33 muestras fueron clasificadas correctamente como clase 0 (True Negatives - TN).
    # No hubo muestras clasificadas incorrectamente como clase 1 o clase 2 (False Positives - FP).

    # Fila 2: Representa la clase 1.
    # 11 muestra fue clasificada correctamente como clase 1 (True Positives - TP).
    # 22 muestras fueron clasificadas incorrectamente como clase 2 (False Negatives - FN).

    # Fila 3: Representa la clase 2.
    # 11 muestra fue clasificada correctamente como clase 2 (TP).
    # 22 muestras fueron clasificadas incorrectamente como clase 1 (FN).

def configrationLogger(disable_logs = False):
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()    
    if disable_logs:
        logger.addHandler(logging.NullHandler())
        logger.setLevel(logging.CRITICAL + 1)
    else:
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
    
    return logger

def downloadDatasets(log, key):  
    datasets = {
        "balance":12,
        "glass":42,
        "ionosphere":52,
        "irisplant":53,
        "wine":109,
        "BCW": 15  
    }
    log.warning("Espera un momento estamos descargando")
    data = fetch_ucirepo(id = datasets[key]) 
    X = data.data.features 
    y = data.data.targets 
    columClass = y.columns.tolist()
    if y[columClass[0]].dtype == 'object':
        y["classification"] = pd.Categorical(y[columClass[0]])
        y["classification"] = y["classification"].cat.codes
    else:
        y['classification'] = y[columClass[0]]
    log.warning("Terminamos la descargar")
    if isinstance(X, pd.DataFrame):
        X =X.to_numpy()
    if isinstance(y, pd.DataFrame):
        y =np.array(y["classification"].tolist())
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42,stratify=y)
    return X_train, X_test, y_train, y_test
