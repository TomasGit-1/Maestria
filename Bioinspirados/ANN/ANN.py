import numpy as np
import pandas as pd
import logging
import math
class ANN():
    logging.basicConfig(level=logging.INFO)
    def __init__(self, X_true, Y_true):
        logging.info("Initialized ANN")
        self.X_true = X_true
        self.Y_true = Y_true
        self.validateConversion()
        self.configuration = [] 
        self.DirectCodificaction()

    def validateConversion(self):
        logging.info("Validando si X and y son nummpy arrasy")
        if isinstance(self.X_true, pd.DataFrame):
            self.X_true =self.X_true.to_numpy()
        if isinstance(self.Y_true, pd.DataFrame):
            self.Y_true =np.array(self.Y_true["class"].tolist())
        
    def DirectCodificaction(self):
        logging.info("Iniciamos la codificación directa")
        self.N = self.X_true.shape[1]
        valores, conteos = np.unique(self.Y_true, return_counts=True)
        self.M = valores.shape[0]
        Q = math.ceil((self.N + self.M) + ((self.M + self.N) / 2))

        logging.info("Generating inputlayer , hidden layer and output layer")
        self.hiddenLayers = Q - (self.M + self.N)
        self.inputLayer = self.N
        self.outputLayer = self.M

        logging.info("Generating dim")
        self.dim = (self.hiddenLayers * (self.N + 3)) + (self.outputLayer * (self.hiddenLayers +3))
        self.param_e_o = self.hiddenLayers * (self.N + 3)
        self.param_o_s = self.outputLayer * (self.hiddenLayers + 3)
        
        logging.info("Generating weights and biases")
        self.W_hidden = []
        self.bias_hidden = []

        self.configurationHL = [{
            "capa": i,
            "T": list(range(0, self.param_e_o)),
            "W" : self.initialize_weights(self.N, self.M),
            "B" : self.initialize_biases(self.M),
            "TF": np.random.randint(0, 6)
        } for i in range(self.hiddenLayers)]

        logging.info("Generating configuration output layer")
        self.configurationOL = [{
            "capa":i,
            "T" : list(range(0, self.param_o_s)),
            "W" : self.initialize_weights(self.N, self.M),
            "B" : self.initialize_biases(self.M),
            "TF": np.random.randint(0,6)
        }for i in range(self.outputLayer)]
         
        
    def forward(self):
        activations = []
        logging.info("Forward cappas ocultas")
        for i in range(self.hiddenLayers):
            activationFunc = self.ActivationFunctions(self.configurationHL[i]["TF"])
            hidden_input = np.dot(self.X_true, self.configurationHL[i]["W"]) + self.configurationHL[i]["B"]
            hidden_output = activationFunc["fx"](hidden_input)
            activations.append(hidden_output)
        
        # Capa de salida
        outputs = []
        for i in range(self.outputLayer):
            output_activation = self.ActivationFunctions(self.configurationOL[i]["TF"])
            final_output = np.dot(activations[-1],  self.configurationOL[i]["W"] +  self.configurationOL[i]["B"])
            Y_pred = output_activation["fx"](final_output)
            outputs.append(Y_pred)

        return outputs
    
    def train(self):
        hidden_output = self.forward()
        print(hidden_output)
      
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

    def initialize_weights(self, N, M):
        return np.random.randn(N, M)


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