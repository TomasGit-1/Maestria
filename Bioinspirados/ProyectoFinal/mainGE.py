import numpy as np
from ParametrosRed import ParametrosRed
from utils import configrationLogger, downloadDatasets, plot_confusion_matrix


log = configrationLogger(disable_logs=True)


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = downloadDatasets(log, "BCW")
    N=X_train.shape[1]
    valores, conteos = np.unique(y_train, return_counts=True)
    M = valores.shape[0]
    #Es el tamanio de la poblacion
    ns  = 1
    PR= ParametrosRed(N,M,ns)
    population=PR.Poblacion()
    pass