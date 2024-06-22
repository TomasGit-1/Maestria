import numpy as np

class ANN():
    def __init__(self, inputLayer, hiddenLayers, outputLayer,learningRate,X_true, Y_true):
        print("Iniciamos las red neuronales")
        self.inputLayer = inputLayer
        self.hiddenLayers = hiddenLayers
        self.outputLayer = outputLayer
        self.learningRate = learningRate
        self.X_true = X_true
        self.Y_true = Y_true

    def activationFuntions(self, ID=0):
        activationFuntions ={
            0:{"name":"Logistic",          "Label":"LS",  "fx": self.logistic},
            1:{"name":"Hyperbolic Tangent","Label":"HT",  "fx": self.tanhiper},
            2:{"name":"Sinusoidal",        "Label":"SN",  "fx": self.sinusoidal},
            3:{"name":"Gaussian",          "Label":"GS",  "fx": self.gaussian},
            4:{"name":"Linear",            "Label":"LN",  "fx": self.linear},
            5:{"name":"Hard limit",        "Label":"HL",  "fx": self.HardLimit},
            6:{"name":"RectifiedLinear",   "Label":"RL",  "fx": self.Relu},
        }
        return activationFuntions[ID]

    def train(self):
        opcionFx = self.activationFuntions(1)
        FAx = opcionFx["fx"]
        y = FAx(self.X_true)
        print(f'Función de activación: {opcionFx["name"]}')
        print(f'Entrada: {self.X_true}')
        print(f'Salida: {y}')
        print('---')

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