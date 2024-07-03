import numpy as np
class Individuo():
    def __init__(self, vector=None, numGenertion=0,N=None,M=None,H=None)-> None:
        self.vector = np.round(vector, 2)
        self.fitness = float("inf")
        self.numGenertion = numGenertion
        self.N=N
        self.M=M
        self.H=H