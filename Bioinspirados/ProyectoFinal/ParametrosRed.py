from utils import  downloadDatasets,configrationLogger
from individuo import Individuo
import numpy as np
import math 
import random 

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
        vector_linspace = np.random.uniform(-10,10,size,)
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
