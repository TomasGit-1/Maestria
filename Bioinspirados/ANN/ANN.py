import numpy as np
import pandas as pd
import math
pd.options.mode.chained_assignment = None
class ANN():

    def __init__(self,log, nameDataset, X_true, Y_true,neuronal):
        self.log = log
        self.log.info("Initialized ANN")
        self.nameDataset = nameDataset
        self.X_true = X_true
        self.Y_true = Y_true
        self.numNeuronas = neuronal
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

        for i, hidden_size in enumerate( self.hiddenneuro):
            if i == 0:
                self.W.append(np.random.randn(self.input_size, hidden_size))
            else:
                self.W.append(np.random.randn(self.hiddenneuro[i-1], hidden_size))
            self.b.append(np.zeros((1, hidden_size)))
        

        # self.configurationHL = [{
        #     "W" : np.random.randn(self.input_size ,self.hiddenLayers) if i == 0 else np.random.randn(self.hiddenneuro[i-1], hidden_size),
        #     "B" : np.zeros((1, hidden_size)),
        #     "TF": np.random.randint(0, 7)
        # } for hidden_size, i in enumerate( self.hiddenneuro)]

        pass

        # self.log.info("Generating configuration output layer")
        # self.configurationOL = [{
        #     "capa":i,
        #     "T" : list(range(0, self.param_o_s)),
        #     "W" : np.random.randn(self.input_size ,self.outputLayer),
        #     "B" : np.random.randn(1,self.input_size ),
        #     "TF": np.random.randint(0,7)
        # }for i in range(self.outputLayer)]
        # print()
         
        
    def forward(self):
        try:
            layer_input = self.X_true
            for i in range(len(self.W)):
                layer_output = np.dot(layer_input, self.W[i]) + self.b[i]
                layer_input = self.sigmoid(layer_output)
            return layer_input
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