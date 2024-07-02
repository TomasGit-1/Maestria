import numpy as np
import pandas as pd
import math
# from utils import configrationLogger, downloadDatasets
from functAct import logistic, tanhiper, sinusoidal,gaussian,linear,HardLimit,Relu
pd.options.mode.chained_assignment = None

class Individuo():
    def __init__(self, xInf=0, xSup=0, dim=0, numGenertion=0)-> None:
        self.vector = np.random.uniform(xInf, xSup, size = dim)
        self.fitness = float("inf")
        self.numGenertion = numGenertion

class ANNC():
    def __init__(self,log):
        self.log = log
        self.log.info("Initialized ANNC")
        
    def getData(self,nameDataset, X_true = None, Y_true = None , configNeurons= None,N=None,M=None,H=None):
        self.log.info(f"Update data")
        self.X_true = X_true
        self.nameDataset = nameDataset
        self.Y_true = Y_true
        self.W,self.F_W,self.V,self.F_V = self.generateConfiguracion(self.log, configNeurons, N,M,H)

    def forward_propagation(self):
        try:
            self.log.warning(f"Inicia la funcion for forward propagation")
            x_train = np.column_stack((self.X_true, np.ones((self.X_true.shape[0],1))))
            inp_h = np.dot(x_train, self.W.T)
            out_h = np.zeros(inp_h.shape)
            for i in range(len(self.F_W)):
                fx = self.ActivationFunctions(ID = int(self.F_W[i]))
                Act = fx["fx"](inp_h.T[i])
                out_h.T[i] = Act
            
            out_h_train = np.column_stack((out_h, np.ones((self.X_true.shape[0],1))))
            inp_out = np.dot(out_h_train, self.V.T)
            out_s = np.zeros(inp_out.shape)
            for i in range(len(self.F_V)):
                fx = self.ActivationFunctions(ID = int(self.F_V[i]))
                Act = fx["fx"](inp_out.T[i])
                out_s.T[i] = Act
            softmaxImp = self.softmax(out_s)
            return np.argmax(softmaxImp, axis=1)
        except Exception as e:
            print(str(e))

    def softmax(self,matrix):
        exp_matrix = np.exp(matrix - np.max(matrix, axis=1, keepdims=True))  
        return exp_matrix / exp_matrix.sum(axis=1, keepdims=True)

    def ActivationFunctions(self,ID=0):
        activationFunctions ={
            0:{"name":"Logistic",          "Label":"LS",  "fx": logistic},
            1:{"name":"Hyperbolic Tangent","Label":"HT",  "fx": tanhiper},
            2:{"name":"Sinusoidal",        "Label":"SN",  "fx": sinusoidal},
            3:{"name":"Gaussian",          "Label":"GS",  "fx": gaussian},
            4:{"name":"Linear",            "Label":"LN",  "fx": linear},
            5:{"name":"Hard limit",        "Label":"HL",  "fx": HardLimit},
            6:{"name":"RectifiedLinear",   "Label":"RL",  "fx": Relu},
        }
        return activationFunctions[ID]

    def generateConfiguracion(self,log, x, N, M, H):
        log.info("cod_directa_ANN")
        W = np.zeros((H,(N+1))) #4x6
        V = np.zeros((M,H+1)) #2X5
        F_W = np.zeros(H) #4x1
        F_V = np.zeros(M) #2x1
        #Configracion para las capas ocultas
        log.info("Configracion para las capas ocultas")
        w_skip = N + 3 # 8
        X_hidden = x[0:w_skip*H]
        W, F_W = self.configuration(H, X_hidden, w_skip, W,F_W,N)
        log.info("Configuracion para las capas de salida")
        #Configracion para las capas de salida
        X_Output = x[w_skip*H:]
        w_skip = H + 3 # 7
        V,F_V = self.configuration(M, X_Output, w_skip, V, F_V, H)
        return W,F_W,V,F_V
    
    def configuration(self,layers, x, w_skip, W, F_W, N):
        for h in range(layers):
            tmp = x[h * w_skip : (h * w_skip + w_skip) ]
            T = '{0:0{1}b}'.format(int(tmp[0]), int(N))
            T = [int(bit) for bit in T]
            T = np.array(T[::-1])
            w = tmp[1:tmp.shape[0]-2]
            if w.shape[0] != T.shape[0]:
                #QUitamos el bit menos significativo
                T = T[:T.shape[0]-1]
            w = w * T
            W[h,0:-1] = w
            W[h,-1] = tmp[w_skip-2]
            F_W[h] = tmp[w_skip-1]
        return W,F_W

    def mce(self,y_pred):
        return  np.mean(self.Y_true == y_pred)
    
class EvolutionDFC():
    def __init__(self,log, xInf=None, xSup=None, dim_indi=None, ns=None,problem=None, beta=None, pr=None, t=None,X_pop =None):
        self.log = log
        self.xInf = xInf
        self.xSup = xSup
        self.dim_indi = dim_indi
        self.ns = ns
        self.FObjective = problem
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
    
    def ordenar(self, vector):
        return  sorted(vector, key= lambda x: x.fitness)
    
    def showVector(self, vector):
        for i in range(len(vector)):
            self.log.info(f" {i} fitnees {vector[i].fitness} vector {vector[i].vector} ")

    def fitnees(self):
        #Calculamos el fitness
        y_pred  = self.objANNC.forward_propagation()    
        return self.objANNC.mce(y_pred)
        
    def optimize(self, max_it,X, y):
        errorGeneration = 10
        gen = 0
        X_ = np.copy(self.X_pop)
        # self.showVector(X_)
        X_ = self.ordenar(X_)
        for _ in (range(max_it)):
            for i in range(len(X_)):
                self.objANNC.getData(nameDataset="",X_true=X, Y_true=y,configNeurons=X_[i].vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)
                X_[i].fitness= self.fitnees()
                pop_temp = [ indi for idx, indi in enumerate(X_) if idx != i]
                ui = self.Mutacion(X_[i], pop_temp)
                x_hijo_vector = self.Cruza(ui, X_[i].vector)
                self.objANNC.getData(nameDataset="",X_true=X, Y_true=y,configNeurons=x_hijo_vector,N=X_[i].N,M=X_[i].M,H=X_[i].H)
                x_hijo_fitness = self.fitnees()

                # X_[i].fitness= self.fitnees(self.objANNC)
                # x_hijo_fitness = self.FObjective(x_hijo_vector)
                if x_hijo_fitness < X_[i].fitness:
                    X_[i].vector = x_hijo_vector
                    X_[i].fitness = x_hijo_fitness
            gen +=1
        X_ = self.ordenar(X_)
        # self.showVector(X_)
        return X_


