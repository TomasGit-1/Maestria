
import numpy as np
from ANNC import ANNC
from utils import downloadDatasets
from individuo import Individuo

class EvolutionDFC():
    def __init__(self,log, xInf=None, xSup=None, dim_indi=None, ns=None, beta=None, pr=None, t=None,X_pop =None):
        self.log = log
        self.xInf = xInf
        self.xSup = xSup
        self.dim_indi = dim_indi
        self.ns = ns
        self.beta = beta
        self.pr = pr
        self.t = t
        self.X_pop=X_pop
        self.objANNC = ANNC(log =  log)

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
    
    def CruzaBinomial(self, U,x_actual):
        j_ = np.random.randint(len(U))
        J = []
        J.append(j_)
        nx = len(U)-1
        for j in range(1, nx):
            U01 = np.random.rand()
            if U01< self.pr and j != j_:
                J.append(j)
        descendiente = np.array([U[j] if U[j] in J else x_actual[j] for j in range(len(U))])
        return descendiente
    
    def ordenar(self, vector):
        return  sorted(vector, key= lambda x: x.fitness)
    
    def showVector(self, vector):
        for i in range(len(vector)):
            self.log.info(f" {i} fitnees {vector[i].fitness} vector {vector[i].vector} ")

    def fitness(self, configNeurons= None,N=None,M=None,H=None):
        try:
            #Calculamos el fitness
            self.objANNC.Data(configNeurons=configNeurons,N=N,M=M,H=H)
            y_pred  = self.objANNC.forward_propagation()    
            return self.objANNC.mce(y_pred)
        except Exception as e:
            print(str(e))

    def validacionDatos(self,configNeurons= None,N=None,M=None,H=None):
        """Paso1: Realizar el split de las capas de ocultas y de
        las capas de salida.
        Paso2: Agarrar subvectores N+3, dende la primera posicion es T
        y N+3 es la funcion.
        """
        vector=configNeurons
        N=N
        M=M
        H=H
        w_skip = N + 3
        v_skip = H + 3
        X_hidden = vector[0:w_skip*N]
        X_Output = vector[w_skip*H:]
        for h in range(H):
            tmp =X_hidden[h * w_skip : (h * w_skip + w_skip)]
            tmp[0]= self.condiciones(sup=(2**N)-1,numero=tmp[0])
            tmp[-1]= self.condiciones(sup=6,numero=tmp[-1])
            X_hidden[h * w_skip : (h * w_skip + w_skip)]=tmp
        for m in range(M):
            tmp2 =X_Output[m * v_skip : (m * v_skip + v_skip)]
            tmp2[0]= self.condiciones(sup=(2**H)-1,numero=tmp2[0])
            tmp2[-1]= self.condiciones(sup=6,numero=tmp2[-1])
            X_Output[m * v_skip : (m * v_skip + v_skip)]=tmp2
        self.log.info("Vector1",vector)
        vector[0:w_skip*N]=X_hidden
        vector[w_skip*H:]=X_Output
        self.log.info("Vec2",vector)
        return vector

    def condiciones(self,sup,numero):
        numero=abs(numero)
        if numero>sup:
            return sup
        return numero
        
    def optimize(self, max_it,X, y):
        gen = 0
        self.objANNC.sendDataset(X_true=X, Y_true=y)
        X_ = np.copy(self.X_pop)
        X_ = self.ordenar(X_)
        for _ in (range(max_it)):
            for i in range(len(X_)): 
                X_[i].vector=self.validacionDatos(configNeurons=X_[i].vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)              
                X_[i].fitness= self.fitness(configNeurons=X_[i].vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)
                pop_temp = [ indi for idx, indi in enumerate(X_) if idx != i]
                ui = self.Mutacion(X_[i], pop_temp)
                x_hijo_vector = self.CruzaBinomial(ui, X_[i].vector)
                x_hijo_vector=self.validacionDatos(configNeurons=x_hijo_vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)
                x_hijo_fitness = None
                son_iguales = np.array_equal(X_[i].vector, x_hijo_vector)
                if son_iguales:
                    self.log.error("Padre e hijos iguales")
                else:
                    self.log.info(f"Son diferentes Fitness {gen} : padre {X_[i].fitness} hijo {x_hijo_fitness}")
                    x_hijo_fitness= self.fitness(configNeurons=x_hijo_vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)
                    if x_hijo_fitness > X_[i].fitness:
                        X_[i].vector = x_hijo_vector
                        X_[i].fitness = x_hijo_fitness

            gen +=1
        X_ = self.ordenar(X_)
        return X_


