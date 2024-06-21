import numpy as np

class ANN():
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.weightsHidden = np.random.uniform(-1,0,self.hidden_size)
        self.biasHidden =  np.random.uniform(-1,0,self.hidden_size)

        self.weightsOutput = np.random.uniform(-1,0,self.hidden_size)
        self.biasOutput =  np.random.uniform(-1,0,self.hidden_size)

    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def forward(self, X):
        hLActivation = np.dot(X, self.weightsHidden) + self.biasHidden
        hLOutput = self.sigmoid(hLActivation)
        fOActivation = np.dot(hLOutput, self.weights_output) + self.bias_output
        finalOutput = self.sigmoid(fOActivation)

        error = y - finalOutput
    
    def train(self, X, y, epochs=1000, learning_rate=0.01):

        for epoch in range(epochs):
            hLActivation = np.dot(X, self.weightsHidden) + self.biasHidden
            hLOutput = self.sigmoid(hLActivation)
            fOActivation = np.dot(hLOutput, self.weights_output) + self.bias_output
            finalOutput = self.sigmoid(fOActivation)

            error = y - finalOutput


        
        