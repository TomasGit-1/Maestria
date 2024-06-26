import numpy as np
import pandas as pd
import math

from functAct import logistic, tanhiper, sinusoidal,gaussian,linear,HardLimit,Relu

pd.options.mode.chained_assignment = None
class ANNC():
    def __init__(self,log):

        self.log = log
        self.log.info("Initialized ANNC")
        self.X_true = np.random.rand(10, 5)
        self.x = np.array([ 
            20, 0.1, 0.2, 0.3, 0.4, 0.5,0.6, 5, 
            5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1,
            25, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2 ,2,
            5, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 3,
            10,0.7,0.8,0.9,1.0,1.2,4,
            4,0.7,0.8,0.9,1.0,1.2,5,
        ])

        self.W,self.F_W,self.V,self.F_V = self.generateConfiguracion(self.log, self.x, 5,2,4)

    def generar_sub_array(self,size,parametros):
        T = np.random.randint(0, parametros)
        vector_linspace = np.linspace(0, 2, size)
        TF = np.random.randint(0, 7)
        return np.concatenate(([T], vector_linspace, [TF]))
    
    def generateX(self):
        self.log.info("Iniciamos la codificación directa")
        self.N = self.X_true.shape[1]
        self.numNeuronas = self.Y_true.shape[0]
        valores, conteos = np.unique(self.Y_true, return_counts=True)
        self.M = valores.shape[0]
        Q = math.ceil((self.N + self.M) + ((self.M + self.N) / 2))

        self.log.info("Generating inputlayer , hidden layer and output layer")
        self.hiddenLayers = Q - (self.M + self.N)
        self.input_size  = self.N
        self.outputLayer = self.M

        self.log.info("Generating dim")
        self.dim = (self.hiddenLayers * (self.N + 3)) + (self.outputLayer * (self.hiddenLayers +3))
        self.param_e_o = self.hiddenLayers * (self.N + 3)
        self.param_o_s = self.outputLayer * (self.hiddenLayers + 3)

        self.log.info(f"Training ANN with {self.nameDataset} Nfeactures {self.input_size }  capas ocultas {self.hiddenLayers} capas de salida {self.outputLayer}")
        self.log.info("Generating weights and biases")

        self.W = []
        self.b = []
        self.hiddenneuro = np.random.randint(1, 7, size=self.hiddenLayers-1)

    def forward_propagation(self,X_true, W, V):
        try:
            x_train = np.column_stack((X_true, np.ones((10,1))))
            inp_h = np.dot(x_train, W.T)
            out_h = np.zeros(inp_h.shape)
            for i in range(len(self.F_W)):
                fx = self.ActivationFunctions(ID = int(self.F_W[i]))
                Act = fx["fx"](inp_h.T[i])
                out_h.T[i] = Act
            
            out_h_train = np.column_stack((out_h, np.ones((10,1))))
            inp_out = np.dot(out_h_train, V.T)
            out_s = np.zeros(inp_out.shape)
            for i in range(len(self.F_V)):
                fx = self.ActivationFunctions(ID = int(self.F_V[i]))
                Act = fx["fx"](inp_out.T[i])
                out_s.T[i] = Act

            return out_s
        except Exception as e:
            print(str(e))


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
            w = w * T
            W[h,0:-1] = w
            W[h,-1] = tmp[w_skip-2]
            F_W[h] = tmp[w_skip-1]
        return W,F_W

    def train(self):
        self.forward_propagation(self.X_true, self.W, self.V)
