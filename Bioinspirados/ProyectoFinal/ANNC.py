import numpy as np
import pandas as pd
import math
# from utils import configrationLogger, downloadDatasets
from functAct import logistic, tanhiper, sinusoidal,gaussian,linear,HardLimit,Relu
pd.options.mode.chained_assignment = None
from sklearn.metrics import confusion_matrix,accuracy_score

class ANNC():
    def __init__(self,log):
        self.log = log
        self.log.info("Initialized ANNC")
    
    def sendDataset(self,X_true=None, Y_true=None):
        self.X_true = X_true
        self.Y_true = Y_true

    def Data(self,nameDataset="", configNeurons= None,N=None,M=None,H=None):
        self.log.info(f"Update data")
        self.nameDataset = nameDataset
        self.W,self.F_W,self.V,self.F_V = self.generateConfiguracion(configNeurons, N,M,H)

    def forward_propagation(self):
        try:
            try:
                self.log.warning(f"Inicia la funcion for forward propagation")
                x_train = np.column_stack((self.X_true, np.ones((self.X_true.shape[0],1))))
                inp_h = np.dot(x_train, self.W.T)
                out_h = np.zeros(inp_h.shape)
                for i in range(len(self.F_W)):

                    # if self.F_W[i] > 6 or self.F_W[i] < 0:
                    #     self.F_W[i] = np.random.randint(0,6)

                    fx = self.ActivationFunctions(ID = int(self.F_W[i]))
                    Act = fx["fx"](inp_h.T[i])
                    out_h.T[i] = Act
            except Exception as e:
                self.log.error(f"Forward propagation Hidden layers failed {str(e)}")

            try:
                out_h_train = np.column_stack((out_h, np.ones((self.X_true.shape[0],1))))
                inp_out = np.dot(out_h_train, self.V.T)
                out_s = np.zeros(inp_out.shape)
                for i in range(len(self.F_V)):

                    # if self.F_V[i] > 6 or self.F_V[i] < 0:
                    #     self.F_V[i] = np.random.randint(0,6)

                    fx = self.ActivationFunctions(ID = int(self.F_V[i]))
                    Act = fx["fx"](inp_out.T[i])
                    out_s.T[i] = Act
            except Exception as e:
                self.log.error(f"Forward propagation Hidden layers failed {str(e)}")

            try:
                softmaxImp = self.softmax(out_s)
                predict = np.argmax(softmaxImp, axis=1)
            except Exception as e:
                self.log.error(f"Forward propagation Hidden layers failed {str(e)}")
         
            return predict
        except Exception as e:
            print(str(e))
            return str(e)

    def softmax(self,matrix):
        try:
            exp_matrix = np.exp(matrix - np.max(matrix, axis=1, keepdims=True))  
            return exp_matrix / exp_matrix.sum(axis=1, keepdims=True)
        except Exception as e:
            self.log.error("Softmax genero una")

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

    def generateConfiguracion(self, x, N, M, H):
        try:
            self.log.info("cod_directa_ANN")
            W = np.zeros((H,(N+1))) #4x6
            V = np.zeros((M,H+1)) #2X5
            F_W = np.zeros(H) #4x1
            F_V = np.zeros(M) #2x1
            #Configracion para las capas ocultas
            self.log.info("Configracion para las capas ocultas")
            w_skip = N + 3 # 8
            X_hidden = x[0:w_skip*H]
            W, F_W = self.configuration(H, X_hidden, w_skip, W,F_W,N)
            self.log.info("Configuracion para las capas de salida")
            #Configracion para las capas de salida
            X_Output = x[w_skip*H:]
            w_skip = H + 3 # 7
            V,F_V = self.configuration(M, X_Output, w_skip, V, F_V, H)
            return W,F_W,V,F_V
        except Exception as e:
            print(str(e))
    
    def configuration(self,layers, x, w_skip, W, F_W, N):
        try:
            for h in range(layers):
                tmp = x[h * w_skip : (h * w_skip + w_skip) ]
                T = '{0:0{1}b}'.format(int(tmp[0]), int(N))
                T = [int(bit) for bit in T]
                T = np.array(T[::-1])
                w = tmp[1:tmp.shape[0]-2]
                if w.shape[0] != T.shape[0]:
                    #QUitamos el bit menos significativo
                    T = T[:w.shape[0]]
                w = w * T
                W[h,0:-1] = w
                W[h,-1] = tmp[w_skip-2]
                F_W[h] = tmp[w_skip-1]
            return W,F_W
        except Exception as e:
            print(str(e))

    def mce(self,y_pred):
        try:
            # tn, fp, fn, tp = confusion_matrix(self.Y_true.tolist(), y_pred.tolist()).ravel()
            acc = accuracy_score(self.Y_true, y_pred)
            # print((tp+tn)/(tn+fn+fp+tp))
            # return  np.mean(self.Y_true == y_pred)
            return acc
        except Exception as e:
            print(str(e))