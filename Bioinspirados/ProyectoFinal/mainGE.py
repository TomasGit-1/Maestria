import numpy as np
from ParametrosRed import ParametrosRed
from utils import configrationLogger, downloadDatasets, plot_confusion_matrix
from GramaticaEvolutiva import performMappingProcess,ordenar,generateGeneration
from ANNC import ANNC

log = configrationLogger(disable_logs=True)

if __name__ == '__main__':
    X_train, X_test, y_train, y_test = downloadDatasets(log, "balance")
    N=X_train.shape[1]
    valores, conteos = np.unique(y_train, return_counts=True)
    M = valores.shape[0]
    #Es el tamanio de la poblacion
    ns  = 2
    PR= ParametrosRed(N,M,ns)
    population=PR.Poblaciongenotipo(min_value=1, max_value=10, size_genotipo=500)    
    numGen = 11
    solutionFound = False
    maxError = 1
    objANNC = ANNC(log =  log)
    objANNC.sendDataset(X_true=X_train, Y_true=y_train)
    fitnessList = []
    elmejor = None
    while not solutionFound:
        population = performMappingProcess(population)
        for individe in population:
            objANNC.Data(configNeurons=individe.vector,N=N,M=M,H=individe.H)
            y_pred  = objANNC.forward_propagation()    
            individe.fitness = objANNC.mce(y_pred)
            fitnessList.append(individe.fitness)
        population = ordenar(population)
        #Como el fines es el accurancy queremos el de mayor valor
        fitnessList = sorted(fitnessList, reverse=True)
        if max(fitnessList) >= maxError:
            maxError = max(fitnessList)
            elmejor = population[0]
            solutionFound = True
        else:
            #Generamos una nueva solucion
            population = generateGeneration(population)
    print(f"El mejor individuo {elmejor}")
    pass
