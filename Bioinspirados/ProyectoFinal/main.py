import numpy as np
from EvolutionD import EvolutionDFC
from ANNC import ANNC
from ParametrosRed import ParametrosRed
from utils import configrationLogger, downloadDatasets


log = configrationLogger()



if __name__== "__main__":


    #inicializacion de la población
    X_train, X_test, y_train, y_test = downloadDatasets(log, "balance")
    N=X_train.shape[1]
    valores, conteos = np.unique(y_train, return_counts=True)
    M = valores.shape[0]
    #Es el tamanio de la poblacion
    ns  = 100
    PR= ParametrosRed(N,M,ns)
    population=PR.Poblacion()
    #inicio de la metahuristica
    #Definimos entradas
    #pr Es la probabil5idad de cruza
    t ,beta, pr = 0, 1.4 ,0.4
    #Definimos el numero de generacionses
    max_it = 1000

    ObjEvolutionDFC = EvolutionDFC(
                                log = log,
                                ns=ns, 
                                beta = beta,
                                pr = pr,
                                t = t,
                                X_pop=population)
  
    X_optimize = ObjEvolutionDFC.optimize(max_it=max_it,X=X_train, y=y_train)
    ObjEvolutionDFC.showVector(X_optimize)
    red=ANNC(log=log)
    red.sendDataset(X_true=X_test,Y_true=y_test)
    red.Data(configNeurons= X_optimize[0].vector,N=X_optimize[0].N,M=X_optimize[0].M,H=X_optimize[0].H)
    y_test_predict=red.forward_propagation()
    exactitud=red.mce(y_test_predict)
    log.info(f"{exactitud}")