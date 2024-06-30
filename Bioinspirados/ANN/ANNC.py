import numpy as np
import pandas as pd
import math

from functAct import logistic, tanhiper, sinusoidal,gaussian,linear,HardLimit,Relu

pd.options.mode.chained_assignment = None
class ANNC():
    def __init__(self,log,nameDataset, X_true = None, Y_true = None , configNeurons= None,useDatasets = False):

        self.log = log
        self.log.info("Initialized ANNC")
        self.X_true = X_true
        self.nameDataset = nameDataset
        self.Y_true = Y_true
        if useDatasets:
            self.log.info(f"Using {nameDataset}")
            configNeurons = self.generateConfgNeurons()
            self.W,self.F_W,self.V,self.F_V = self.generateConfiguracion(self.log, configNeurons, self.input_size,self.output_size,self.hidden_size)
        else:
            self.log.info(f"Using manual configuration")
            self.configNeurons = configNeurons
            self.W,self.F_W,self.V,self.F_V = self.generateConfiguracion(self.log, configNeurons, 5,2,4)

        self.log.warning(f" Configuracion \n W: = {self.W} \n F_W: {self.F_W} , \n V: {self.V} \nF_V :{self.F_V} " )

    def generar_sub_array(self,size,parametros):
        T = np.random.randint(0, parametros)
        vector_linspace = np.linspace(0, 2, size)
        TF = np.random.randint(0, 7)
        return np.concatenate(([T], vector_linspace, [TF]))
    
    def generateConfgNeurons(self):
        self.log.info("Iniciamos la codificación directa H oculatas , M salidas, N entradas")
        self.input_size = self.X_true.shape[1]

        valores, conteos = np.unique(self.Y_true, return_counts=True)
        self.output_size = valores.shape[0]
        Q = math.ceil((self.input_size + self.output_size) + ((self.output_size + self.input_size) / 2))

        self.log.info("Generating inputlayer , hidden layer and output layer")
        self.hidden_size= Q - (self.output_size+ self.input_size)


        self.log.info("Generating dim")
        self.dim = (self.hidden_size * (self.input_size + 3)) + (self.output_size * (self.hidden_size +3))
        self.param_e_o = self.hidden_size * (self.input_size + 3)
        self.param_o_s = self.output_size * (self.hidden_size + 3)

        self.log.error(f"Training ANN with {self.nameDataset} Nfeactures {self.input_size }  capas ocultas {self.hidden_size} capas de salida {self.output_size}")
        self.log.info("Generating weights and biases")

        #Creamos el vector X con los datos calculados
        size = self.input_size + 1 #Por el bias 
        x_hidden = np.concatenate([self.generar_sub_array(size,self.param_e_o) for _ in range(self.hidden_size)])
        size = self.hidden_size + 1
        x_output = np.concatenate([self.generar_sub_array(size,self.param_o_s) for _ in range(self.output_size)])
        x = x_hidden.tolist() + x_output.tolist()
        x = np.array(x)
        self.log.info("Genere con base a las formular la neuronas ")
        return x


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
            if w.shape[0] != T.shape[0]:
                #QUitamos el bit menos significativo
                T = T[:T.shape[0]-1]
            w = w * T
            W[h,0:-1] = w
            W[h,-1] = tmp[w_skip-2]
            F_W[h] = tmp[w_skip-1]
        return W,F_W

    def train(self):
        self.forward_propagation(self.X_true, self.W, self.V)

    def accuracy(y_true, y_pred):
        y_pred_rounded = np.round(y_pred)
        accuracy = np.mean(y_true == y_pred_rounded)
        return accuracy
