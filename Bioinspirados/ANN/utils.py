from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from ucimlrepo import fetch_ucirepo 


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


def balance_scale():  
    balance_scale = fetch_ucirepo(id=12) 

    X = balance_scale.data.features 
    y = balance_scale.data.targets 
    return X, y
    # metadata 
    print(balance_scale.metadata) 
    
    # variable information 
    print(balance_scale.variables) 
