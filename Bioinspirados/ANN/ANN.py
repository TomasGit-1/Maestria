import numpy as np
import pandas as pd
import math
pd.options.mode.chained_assignment = None
class ANN():

    def __init__(self,log, nameDataset, X_true, Y_true):
        self.log = log
        self.log.info("Initialized ANN")
        self.nameDataset = nameDataset
        self.X_true = X_true
        self.Y_true = Y_true
        self.validateConversion()
        self.configuration = [] 
        self.DirectCodificaction()

    def validateConversion(self):
        self.log.info("Validando si X and y son nummpy arrasy")
        if isinstance(self.X_true, pd.DataFrame):
            self.X_true =self.X_true.to_numpy()
        if isinstance(self.Y_true, pd.DataFrame):
            self.Y_true =np.array(self.Y_true["classification"].tolist())
        
    def DirectCodificaction(self):
        
        self.log.info("Iniciamos la codificación directa")
        self.N = self.X_true.shape[1]
        self.numNeuronas = self.Y_true.shape[0]
        valores, conteos = np.unique(self.Y_true, return_counts=True)
        self.M = valores.shape[0]
        Q = math.ceil((self.N + self.M) + ((self.M + self.N) / 2))

        self.log.info("Generating inputlayer , hidden layer and output layer")
        self.hiddenLayers = Q - (self.M + self.N)
        self.inputLayer = self.N
        self.outputLayer = self.M

        self.log.info("Generating dim")
        self.dim = (self.hiddenLayers * (self.N + 3)) + (self.outputLayer * (self.hiddenLayers +3))
        self.param_e_o = self.hiddenLayers * (self.N + 3)
        self.param_o_s = self.outputLayer * (self.hiddenLayers + 3)

        self.log.info(f"Training ANN with {self.nameDataset} capas de entrada {self.N}  capas ocultas {self.hiddenLayers} capas de salida {self.outputLayer}")

        mask = np.random.randint(0, 2, (10, 7))  # Example mask for 10 input neurons to 7 hidden neurons
        
        self.log.info("Generating weights and biases")
        self.configurationHL = [{
            "capa": i,
            "T": list(range(0, self.param_e_o)),
            "W" : np.random.randn(self.numNeuronas,self.N),
            "B" : np.random.randn(self.numNeuronas,1),
            "TF": np.random.randint(0, 7)
        } for i in range(self.hiddenLayers)]

        self.log.info("Generating configuration output layer")
        self.configurationOL = [{
            "capa":i,
            "T" : list(range(0, self.param_o_s)),
            "W" : np.random.randn(self.numNeuronas,self.N),
            "B" : np.random.randn(self.numNeuronas,1),
            "TF": np.random.randint(0,7)
        }for i in range(self.outputLayer)]
        print()
         
        
    def forward(self):
        try:
            activations = []
            x = self.X_true.T
            self.log.info("Forward cappas ocultas")
            for i in range(self.hiddenLayers):
                activationFunc = self.ActivationFunctions(self.configurationHL[i]["TF"])
                y_predict = np.dot(x, self.configurationHL[i]["W"]) #+ self.configurationHL[i]["B"]
                resulAc = activationFunc["fx"](y_predict)
                activations.append(resulAc)
                x = resulAc
            
            # Capa de salida
            outputs = []
            for i in range(self.outputLayer):
                output_activation = self.ActivationFunctions(self.configurationOL[i]["TF"])
                final_output = np.dot(activations[-1],  self.configurationOL[i]["W"] +  self.configurationOL[i]["B"])
                Y_pred = output_activation["fx"](final_output)
                outputs.append(Y_pred)
            return outputs
        except Exception as e:
            self.log.error(f"Ocurrio un problema en forward {str(e)}")
    
    def train(self):
        hidden_output = self.forward()
      
    def ActivationFunctions(self, ID=0):
        activationFunctions ={
            0:{"name":"Logistic",          "Label":"LS",  "fx": self.logistic},
            1:{"name":"Hyperbolic Tangent","Label":"HT",  "fx": self.tanhiper},
            2:{"name":"Sinusoidal",        "Label":"SN",  "fx": self.sinusoidal},
            3:{"name":"Gaussian",          "Label":"GS",  "fx": self.gaussian},
            4:{"name":"Linear",            "Label":"LN",  "fx": self.linear},
            5:{"name":"Hard limit",        "Label":"HL",  "fx": self.HardLimit},
            6:{"name":"RectifiedLinear",   "Label":"RL",  "fx": self.Relu},
        }
        return activationFunctions[ID]

    def initialize_weights(self,):
        return np.random.randn(self.N)

    def mean_squared_error(y_pred, y_true):
        return np.mean((y_pred - y_true) ** 2)

    def initialize_biases(self, M):
        # Inicialización de sesgos a cero
        return np.zeros((1, M))
    
    def logistic(self, x):
        return 1 / (1 + np.exp(-x))
    
    def tanhiper(self,x):
        return np.tanh(x)
    
    def sinusoidal(self, x):
        return np.sin(x)

    def gaussian(self, x):
        return np.exp(- (x ** 2))

    def linear(self, x):
        return x

    def HardLimit(self, x):
        return np.where(x >= 0, 1, 0)
    
    def Relu(self, x):
        return np.maximum(0, x)