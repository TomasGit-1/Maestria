import numpy as np
import logging
from colorlog import ColoredFormatter

logger = logging.getLogger()
logger.setLevel(logging.INFO) 

formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def configuration(layers, x, w_skip, W, F_W, N):
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

def cod_directa_ANN(log, x, N, M, H):
    log.info("cod_directa_ANN")
    W = np.zeros((H,(N+1))) #4x6
    V = np.zeros((M,H+1)) #2X5
    F_W = np.zeros(H) #4x1
    F_V = np.zeros(M) #2x1
    #Configracion para las capas ocultas
    log.info("Configracion para las capas ocultas")
    w_skip = N + 3 # 8
    X_hidden = x[0:w_skip*H]
    W, F_W = configuration(H, X_hidden, w_skip, W,F_W,N)
    log.info("COnfiguracion para las capas de salida")
    #Configracion para las capas de salida
    X_Output = x[w_skip*H:]
    w_skip = H + 3 # 7
    V,F_V = configuration(M, X_Output, w_skip, V, F_V, H)
    return W,F_W,V,F_V

def generar_sub_array(size,parametros):
        T = np.random.randint(0, parametros)
        vector_linspace = np.linspace(0, 2, size)
        TF = np.random.randint(0, 7)
        return np.concatenate(([T], vector_linspace, [TF]))

def logistic(x):
        return 1 / (1 + np.exp(-x))
    
def tanhiper(x):
    return np.tanh(x)

def sinusoidal(x):
    return np.sin(x)

def gaussian(x):
    return np.exp(- (x ** 2))

def linear(x):
    return x

def HardLimit(x):
    return np.where(x >= 0, 1, 0)

def Relu(x):
    return np.maximum(0, x)

def ActivationFunctions(ID=0):
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
def forward_propagation(X_true, W, V):
    try:
        hidden = []

        x_train = np.column_stack((X_true, np.ones((10,1))))
        inp_h = np.dot(x_train, W.T)
        out_h =1 #Aplicar la funcion de activacion por columna
        for i in W:
            w = i[:len(i)-2]
            b = i[-2]
            fxId = i[-1] 
            inp_h1 = np.dot(x_train, w.T) + b
            fx = ActivationFunctions(ID = int(fxId))
            Act = fx["fx"](inp_h1)
            hidden.append(Act)
            # x_train = inp_h1
        output = []
        hidden = np.array(hidden)
        for i in V:
            w = i[:len(i)-2]
            b = i[-2]
            fxId = i[-1] 
            inp_h1 = np.dot(hidden, w) + b
            fx = ActivationFunctions(ID = int(fxId))
            Act = fx["fx"](inp_h1)
            output.append(Act)

        return output
    except Exception as e:
        print(str(e))
         

if __name__ == "__main__":
    log = logger
    x = np.array([ 
                20,0.1,0.2,0.3,0.4,0.5,0.6,5, 
                5,0.7,0.8,0.9,1.0,1.1,1.2,1,
                25,0.7,0.8,0.9,1.0,1.1,1.2,2,
                5,0.7,0.8,0.9,1.0,1.1,1.2,3,
                10,0.7,0.8,0.9,1.0,1.2,4,
                4,0.7,0.8,0.9,1.0,1.2,5,
                ])

    W,F_W,V,F_V = cod_directa_ANN(log, x, 5,2,4)
    log.info("Weights hidden ")
    print(W)
    print(F_W)
    log.info("Weights output ")
    print(V)
    print(F_V)
    forward_propagation(np.random.rand(10, 5), W, V)
    