from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 
import pandas as pd

def generateSample(n_features, n_classes):
    random_state = 42 
    X, y = make_classification(n_samples=10, n_features=n_features, n_informative=3,
                            n_redundant=1, n_classes=n_classes, random_state=random_state)
    return X, y
    
def paintXYPlot(X,y):
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=y, marker='o', s=50, edgecolors='k', cmap='viridis')
    plt.title('Dataset con 4 características y 3 clases')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.colorbar()
    plt.show()


def downloadDatasets(log, key):  
    datasets = {
        "balance":12,
        "glass":42,
        "ionosphere":52,
        "irisplant":53,
        "wine":109
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

    return X, y

