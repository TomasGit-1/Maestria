
import numpy as np

class Individuo():
    def __init__(self, xInf=0, xSup=0, dim=0, numGenertion=0)-> None:
        self.vector = np.random.uniform(xInf, xSup, size = dim)
        self.fitness = float("inf")
        self.numGenertion = numGenertion

class EvolutionDFC():
    def __init__(self, xInf, xSup, dim_indi, ns,problem, beta, pr, t ):
        self.xInf = xInf
        self.xSup = xSup
        self.dim_indi = dim_indi
        self.ns = ns
        self.FObjective = problem
        self.beta = beta
        self.pr = pr
        self.t = t

    def generatePopulation(self):
        self.X_pop = np.array(
            [Individuo(xInf=self.xInf, 
                                xSup=self.xSup, dim=self.dim_indi,
                                numGenertion = self.t) 
                            for _ in range(self.ns)])
    
    def Mutacion(self,xi, pop_temp):
        selecion = np.random.choice(pop_temp,size=2,replace=False)
        x2 = selecion[0]
        x3 = selecion[1]
        ui = xi.vector + self.beta * (x2.vector - x3.vector)
        return ui
    
    def Cruza(self, U , x_actual):
        #Cruza Exponencial
        J = []
        nx = len(U)-1
        j = np.random.normal(0, nx)

        while True:
            J.append(j+1)
            j = (j + 1) % nx
            #round(np.random.rand(), 4)
            U01 = np.random.rand()
            if U01 >= self.pr or len(J) == nx:
                break
        return np.array([U[j] if U[j] in J else x_actual[j] for j in range(len(U))])
    
    def ordenar(self, vector):
        return  sorted(vector, key= lambda x: x.fitness)
        
    def optimize(self, max_it):
        errorGeneration = 10
        gen = 0
        X_ = np.copy(self.X_pop)
        X_ = self.ordenar(X_)
        for i in (range(max_it)):
            print(f"Generacion {gen}")
            for i in range(len(X_)):
                X_[i].fitness = self.FObjective(X_[i].vector)
                pop_temp = [ indi for idx, indi in enumerate(X_) if idx != i]
                ui = self.Mutacion(X_[i], pop_temp)
                x_hijo_vector = self.Cruza(ui, X_[i].vector)
                x_hijo_fitness = self.FObjective(x_hijo_vector)
                if x_hijo_fitness < X_[i].fitness:
                    X_[i].vector = x_hijo_vector
                    X_[i].fitness = x_hijo_fitness
            gen +=1
        X_ = self.ordenar(X_)
        return X_

def objective_function(vector):
    return np.sum(vector**2)

if __name__ == '__main__':
    individuos = 100
    """verificar si es la esntarda de la redº"""
    # xInf, xSup = np.repeat(-5.12,d),np.repeat(5.12,d)
    xInf, xSup, dim_indi = -5.12,5.12, 5

    #Definimos entradas
    #pr Es la probabilidad de cruza
    t ,beta, pr = 0, 1.4 ,0.4
    #Definimos el numero de generacionses
    max_it = 1000

    #Es el tamanio de la poblacion
    ns  =10
    ObjEvolutionDFC = EvolutionDFC(
                                xInf=xInf,
                                xSup=xSup,
                                dim_indi=dim_indi, 
                                ns=ns, 
                                problem=objective_function,
                                beta = beta,
                                pr = pr,
                                t = t)
    ObjEvolutionDFC.generatePopulation()
    ObjEvolutionDFC.optimize(max_it=max_it)




