import numpy as np
import pandas as pd
import math
pd.options.mode.chained_assignment = None

class RedNeuronalModel():
    def __init__(self,log, X_true, Y_true,):
        self.log = log
        self.log.info("Initialized RedNeuronalModel")
        self.X_true = np.random.rand(10, 4)
        self.Y_true = Y_true
        self.learning_rate = 0.1
        self.validateConversion()

        """Definimos las entradas de mi red"""
        self.input_size =  self.X_true.shape[1]
        valores, conteos = np.unique(self.Y_true, return_counts=True)
        self.output_size = valores.shape[0]
        #Hidden size
        Q = math.floor((self.input_size + self.output_size) + ((self.output_size + self.input_size / 2)))
        self.hidden_size = Q - (self.output_size + self.input_size)
        
        self.dim = (self.hidden_size * (self.input_size + 3)) + (self.output_size * (self.hidden_size +3))
        self.param_e_o = self.hidden_size * (self.input_size + 3)
        self.param_o_s = self.output_size * (self.hidden_size + 3)

        #Creamos el vector X con los datos calculados
        size = self.input_size + 1 #Por el bias 
        x_hidden = np.concatenate([self.generar_sub_array(size,self.param_e_o) for _ in range(self.hidden_size)])
        size = self.hidden_size + 1
        x_output = np.concatenate([self.generar_sub_array(size,self.param_o_s) for _ in range(self.output_size)])
        x = x_hidden.tolist() + x_output.tolist()
        x = np.array(x)

        x = np.array([ 
                    20,0.1,0.2,0.3,0.4,0.5,0.6,5, 
                    5,0.7,0.8,0.9,1.0,1.1,1.2,1,
                    25,0.7,0.8,0.9,1.0,1.1,1.2,2,
                    5,0.7,0.8,0.9,1.0,1.1,1.2,3,
                    10,0.7,0.8,0.9,1.0,1.2,4,
                    4,0.7,0.8,0.9,1.0,1.2,5,
                    ])
        
        self.W,self.F_W,self.V,self.F_V = self.cod_directa_ANN(x, 5,2,4)

        # x, N, M, H
        # self.W,self.F_W,self.V,self.F_V  = self.cod_directa_ANN(x, 
        #                                         self.input_size, 
        #                                         self.output_size, 
        #                                         self.hidden_size)

    
    def generar_sub_array(self,size,parametros):
        T = np.random.randint(0, parametros)
        vector_linspace = np.linspace(0, 2, size)
        TF = np.random.randint(0, 7)
        return np.concatenate(([T], vector_linspace, [TF]))

    def cod_directa_ANN(self,x, N, M, H):
        self.log.info("cod_directa_ANN")
        W = np.zeros((H,(N+1))) #4x6
        V = np.zeros((M,H+1)) #2X5
        F_W = np.zeros(H) #4x1
        F_V = np.zeros(M) #2x1
        
        #Configracion para las capas ocultas
        self.log.info("Configracion para las capas ocultas")
        w_skip = N + 3 # 8
        X_hidden = x[0:w_skip*H]
        W,F_W = self.configuration(H, X_hidden, w_skip, W,F_W,N)
        self.log.info("COnfiguracion para las capas de salida")
        #Configracion para las capas de salida
        X_Output = x[w_skip*H:]
        w_skip = H + 3 # 7
        V,F_V = self.configuration(M, X_Output, w_skip, V, F_V, H)
        return W,F_W,V,F_V

    def configuration(self, layers, x, w_skip, W, F_W, N):
        for h in range(layers):
            tmp = x[h * w_skip : (h * w_skip + w_skip) ]
            T = '{0:0{1}b}'.format(int(tmp[0]), int(N))
            T = [int(bit) for bit in T]
            T = np.array(T[::-1])
            w = tmp[1:tmp.shape[0]-2]
            w = w * T
            W[h,0:-1] = w
            W[h,-1] = tmp[w_skip-2]
            F_W[-1] = tmp[-1]
        return W,F_W

    def validateConversion(self):
        self.log.info("Validando si X and y son nummpy arrasy")
        if isinstance(self.X_true, pd.DataFrame):
            self.X_true =self.X_true.to_numpy()
        if isinstance(self.Y_true, pd.DataFrame):
            # self.Y_true['classification'] = self.Y_true['classification'].apply(np.array)
            self.Y_true['classification'] = self.Y_true['classification'].apply(lambda x: np.array(x) if isinstance(x, list) else np.array([x]))
            self.Y_true =np.array(self.Y_true["classification"].tolist())
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def initialize_weights(self):
        np.random.seed(42)
        W1 = np.random.randn(self.input_size, self.hidden_size)
        mask = np.random.rand(self.input_size, self.hidden_size) < self.connectivity
        W1 *= mask   
        W2 = np.random.randn(self.hidden_size, self.output_size)
        return W1, W2
    
    def forward_propagation(self):
        activacion = []
        x_train = self.X_true
        for i in self.W:
            w = i[:len(i)-2]
            b = i[-2]
            fxId = i[-1] 
            inp_h1 = np.dot(x_train, w) + b
            fx = self.ActivationFunctions(ID = int(fxId))
            Act = fx["fx"](inp_h1)
            activacion.append(Act)
            # x_train = inp_h1

        for i in self.V:
            w = i[:len(i)-2]
            b = i[-2]
            fxId = i[-1] 
            inp_h1 = np.dot(x_train, w) + b
            fx = self.ActivationFunctions(ID = int(fxId))
            Act = fx["fx"](inp_h1)
            activacion.append(Act)

        self.Z2 = np.dot(self.A1, self.W2)
        self.A2 = self.sigmoid(self.Z2)
        return self.A2
    
    def train(self,epochs):
        for epoch in range(epochs):
            self.forward_propagation()
            if epoch % 1000 == 0:
                loss = np.mean((self.Y_true - self.A2) ** 2)
                print(f"Epoch {epoch}, Loss: {loss}")
    
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
    
    def predict(self):
        return self.forward_propagation()
    #Funciones de activacion
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