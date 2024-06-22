import numpy as np
import logging
import math
class ANN():
    logging.basicConfig(level=logging.INFO)
    def __init__(self, X_true, Y_true):
        logging.info("Initialized ANN")
        self.X_true = X_true
        self.Y_true = Y_true
        self.configuration = [] 
        self.DirectCodificaction()


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

        self.configurationHL = []
        for i in range(self.hiddenLayers):
            tempConfiguration ={
                "capa":i,
                "T" : list(range(0, self.param_e_o)),
                "W" : np.random.randn(self.N, self.M),
                "B" : np.zeros((1, self.M)),
                "TF": np.random.randint(0,6)
            }
            self.configurationHL.append(tempConfiguration)
            
        logging.info("Generating configuration output layer")
        self.configurationOL = []
        for i in range(self.outputLayer):
            tempConfiguration ={
                "capa":i,
                "T" : list(range(0, self.param_o_s)),
                "W" : np.random.randn(self.N, self.M),
                "B" : np.zeros((1, self.M)),
                "TF": np.random.randint(0,6)
            }
            self.configurationOL.append(tempConfiguration)
        
    def forward(self):
        #Implementation de una sola capa
        # activationFunc = self.ActivationFunctions(6)
        # hidden_input = np.dot(self.X_true, self.W) + self.b
        # hidden_output = activationFunc["fx"](hidden_input)
        # return hidden_output
        activations = []
        logging.info("Forward cappas ocultas")
        for i in range(self.hiddenLayers):
            activationFunc = self.ActivationFunctions(self.configurationHL[i]["TF"])
            hidden_input = np.dot(self.X_true, self.configurationHL[i]["W"]) + self.configurationHL[i]["B"]
            hidden_output = activationFunc["fx"](hidden_input)
            activations.append(hidden_output)
        
        # Capa de salida
        for i in range(self.outputLayer):
            output_activation = self.ActivationFunctions(self.configurationOL[i]["TF"])
            final_output = np.dot(self.X_true,  self.configurationHL[i]["W"] +  self.configurationHL[i]["B"])
            Y_pred = output_activation["fx"](final_output)

        return Y_pred
    
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