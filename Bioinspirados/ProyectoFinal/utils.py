from colorlog import ColoredFormatter
from ucimlrepo import fetch_ucirepo 
import pandas as pd
import logging
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def plot_classification(X, y):
    # Obtener clases únicas
    classes = np.unique(y)
    
    # Definir colores para las clases
    colors = plt.cm.rainbow(np.linspace(0, 1, len(classes)))
    
    # Graficar cada clase
    plt.figure(figsize=(8, 6))
    for i, class_label in enumerate(classes):
        # Filtrar datos para esta clase
        class_data = X[y == class_label]
        plt.scatter(class_data[:, 0], class_data[:, 1], color=colors[i], label=f'Clase {int(class_label)}')
    
    # Configuración del gráfico
    plt.title('Gráfico de Clasificación')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Ejemplo de uso
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5], [1, 3], [2, 4], [3, 5], [4, 6]])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1])


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


    return X, y

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
