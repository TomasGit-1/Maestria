import numpy as np
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