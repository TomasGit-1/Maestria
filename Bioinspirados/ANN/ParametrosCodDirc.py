import numpy as np
import math 
from utils import  downloadDatasets,configrationLogger
import random 
from ANNC import ANNC
log = configrationLogger()

class Individuo():
    def __init__(self, vector=None, numGenertion=0,N=None,M=None,H=None)-> None:
        self.vector = vector
        self.fitness = float("inf")
        self.numGenertion = numGenertion
        self.N=N
        self.M=M
        self.H=H

class ParametrosRed():
    def __init__(self,N,M,Pob_size)-> None:
        self.N=N
        self.M=M
        self.Q =math.ceil((self.N+self.M)+((self.M+self.N)/2))
        self.H=self.Q-(self.N+self.M)
        self.dim= (self.H* (self.N+3))+(self.M*(self.H+3))
        self.dim_eo=self.H* (self.N+3)
        self.dim_os=self.M*(self.H+3)
        self.dim_pesos= self.H
        self.Pob_size=Pob_size

    def Individuo(self,size):
        self.T=2**(self.N)
        funcion_act= random.randint(0,6)
        Tr= random.randint(0,self.T-1)
        vector_linspace = np.linspace(-10,10,size, dtype=np.float32)
        bias= np.random.rand()
        return np.concatenate(([Tr], vector_linspace,[bias], [funcion_act]))

    def Poblacion(self):
        #Creamos el vector X con los datos calculados
        Population= []
        for i in range(self.Pob_size):
            x_hidden = np.concatenate([self.Individuo(self.N) for _ in range(self.H)])
            x_output = np.concatenate([self.Individuo(self.H) for _ in range(self.M)])
            x = x_hidden.tolist() + x_output.tolist()
            Population.append(Individuo(np.array(x),0,self.N,self.M,self.H))

        return Population



if __name__== "__main__":

    X, y = downloadDatasets(log, "wine")
    N=X.shape[1]
    valores, conteos = np.unique(y, return_counts=True)
    M = valores.shape[0]
    PR= ParametrosRed(N,M,1)
    # print(PR.H,PR.dim,PR.dim_eo,PR.dim_os)
    Population = PR.Poblacion()
    log.warning("wine")
    log.info(f"Info N:{N} - M :{M} - H : {PR.H} - dim: {PR.dim} - dim_eo: {PR.dim_eo} - dim_os {PR.dim_os}")
    log.info(f"Vector: {Population[0].vector}")
    