from ANNC import ANNC
from utils import configrationLogger, downloadDatasets
import numpy as np

if __name__ == "__main__":
    log = configrationLogger()
    useDatasets = True
    if useDatasets:
        nameDataset = "ionosphere"
        #Empezamos a descargar el datsets
        X, y = downloadDatasets(log, nameDataset)
        configNeurons = None
    else:
        nameDataset = "Manual"
        #Ocupamos un vector y X estatico
        configNeurons = np.array([ 
                20, 0.1, 0.2, 0.3, 0.4, 0.5,0.6, 5, 
                5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1,
                25, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2 ,2,
                5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 3,
                10,0.7,0.8,0.9,1.0,1.2,4,
                4,0.7,0.8,0.9,1.0,1.2,5,
            ])
        X = np.random.rand(10, 5)
        y = np.random.randint(2, size=10)

    objANNC = ANNC(log,nameDataset, X, y , configNeurons,useDatasets)
    objANNC.forward_propagation()
