import numpy as np
from ED import EvolutionDFC
from ANNC import ANNC
from ParametrosCodDirc import ParametrosRed
from utils import configrationLogger, downloadDatasets
log = configrationLogger()


def objective_function(vector):
    return np.sum(vector**2)


if __name__== "__main__":
    #inicializacion de la población
    X, y = downloadDatasets(log, "balance")
    N=X.shape[1]
    valores, conteos = np.unique(y, return_counts=True)
    M = valores.shape[0]
    #Es el tamanio de la poblacion
    ns  =10
    PR= ParametrosRed(N,M,ns)
    population=PR.Poblacion()
    #inicio de la metahuristica
    #Definimos entradas
    #pr Es la probabilidad de cruza
    t ,beta, pr = 0, 1.4 ,0.2
    #Definimos el numero de generacionses
    max_it = 100

    
    ObjEvolutionDFC = EvolutionDFC(
                                log = log,
                                ns=ns, 
                                problem=objective_function,
                                beta = beta,
                                pr = pr,
                                t = t,
                                X_pop=population)
  
    X_optimize = ObjEvolutionDFC.optimize(max_it=max_it,X=X, y=y)
    ObjEvolutionDFC.showVector(X_optimize)
    