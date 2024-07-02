import numpy as np
from EvolutionD import EvolutionDFC
from ANNC import ANNC
from ParametrosRed import ParametrosRed
from utils import configrationLogger, downloadDatasets
log = configrationLogger()


if __name__== "__main__":
    #inicializacion de la población
    X, y = downloadDatasets(log, "balance")
    N=X.shape[1]
    valores, conteos = np.unique(y, return_counts=True)
    M = valores.shape[0]
    #Es el tamanio de la poblacion
    ns  =4
    PR= ParametrosRed(N,M,ns)
    population=PR.Poblacion()
    #inicio de la metahuristica
    #Definimos entradas
    #pr Es la probabilidad de cruza
    t ,beta, pr = 0, 1.4 ,0.9
    #Definimos el numero de generacionses
    max_it = 100

    
    ObjEvolutionDFC = EvolutionDFC(
                                log = log,
                                ns=ns, 
                                beta = beta,
                                pr = pr,
                                t = t,
                                X_pop=population)
  
    X_optimize = ObjEvolutionDFC.optimize(max_it=max_it,X=X, y=y)
    # ObjEvolutionDFC.showVector(X_optimize)
    